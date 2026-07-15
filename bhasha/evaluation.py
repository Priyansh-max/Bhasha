from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .asr.faster_whisper_backend import FasterWhisperASR
from .mos import MOSRating, aggregate_mos_ratings, parse_mos_score
from .reporting import write_benchmark_csv, write_json
from .speaker.speechbrain_backend import SpeechBrainSpeakerEmbedding
from .speaker_metrics import cosine_similarity
from .text_metrics import character_error_rate, normalize_text, word_error_rate


def evaluate_asr(
    run_dir: str | Path,
    *,
    model_size: str = "tiny",
    device: str = "cpu",
    compute_type: str = "int8",
) -> Path:
    run_path = Path(run_dir)
    benchmark_path = run_path / "benchmark.csv"
    if not benchmark_path.exists():
        raise FileNotFoundError(f"Benchmark CSV not found: {benchmark_path}")

    rows = _read_benchmark_csv(benchmark_path)
    backend = FasterWhisperASR(model_size=model_size, device=device, compute_type=compute_type)
    transcripts: list[dict[str, Any]] = []

    for row in rows:
        if row.get("status") != "success" or not row.get("output_audio"):
            continue

        audio_path = _resolve_audio_path(run_path, row["output_audio"])
        if not audio_path.exists():
            row["failure_type"] = row.get("failure_type") or "model_error"
            row["failure_reason"] = f"Audio file missing during ASR evaluation: {audio_path}"
            continue

        transcript = backend.transcribe(audio_path, language=row.get("language") or None)
        wer = word_error_rate(row.get("input_text", ""), transcript.text)
        cer = character_error_rate(row.get("input_text", ""), transcript.text)

        row["asr_model"] = backend.model_label
        row["asr_transcript"] = transcript.text
        row["wer"] = round(wer, 6)
        row["cer"] = round(cer, 6)

        transcripts.append(
            {
                "sample_id": row.get("sample_id"),
                "language": row.get("language"),
                "input_text": row.get("input_text"),
                "normalized_input_text": normalize_text(row.get("input_text", "")),
                "asr_transcript": transcript.text,
                "normalized_asr_transcript": normalize_text(transcript.text),
                "wer": round(wer, 6),
                "cer": round(cer, 6),
                "asr_model": backend.model_label,
                "audio_path": str(audio_path),
                "detected_language": transcript.language,
                "asr_duration_seconds": transcript.duration_seconds,
            }
        )

    write_benchmark_csv(benchmark_path, rows)
    write_json(run_path / "transcripts.json", transcripts)
    return benchmark_path


def _read_benchmark_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def _resolve_audio_path(run_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute() or path.exists():
        return path

    candidate = run_dir / path
    if candidate.exists():
        return candidate

    # Existing rows store paths relative to the project root, so cwd-relative is the common case.
    return path


def evaluate_speaker_similarity(
    run_dir: str | Path,
    *,
    model_source: str = "speechbrain/spkrec-ecapa-voxceleb",
    savedir: str = "models/speaker/speechbrain-spkrec-ecapa-voxceleb",
    device: str = "cpu",
) -> Path:
    run_path = Path(run_dir)
    benchmark_path = run_path / "benchmark.csv"
    if not benchmark_path.exists():
        raise FileNotFoundError(f"Benchmark CSV not found: {benchmark_path}")

    rows = _read_benchmark_csv(benchmark_path)
    backend: SpeechBrainSpeakerEmbedding | None = None
    backend_label = f"speechbrain:{model_source}:{device}"
    similarities: list[dict[str, Any]] = []

    for row in rows:
        if row.get("status") != "success" or not row.get("output_audio"):
            continue
        if row.get("speaker_similarity") == "not_applicable":
            row["speaker_embedding_model"] = "not_applicable"
            continue

        reference_audio = row.get("reference_audio") or ""
        if not reference_audio:
            row["speaker_embedding_model"] = backend_label
            row["speaker_similarity"] = "missing_reference_audio"
            continue

        reference_path = _resolve_audio_path(run_path, reference_audio)
        output_path = _resolve_audio_path(run_path, row["output_audio"])

        if not reference_path.exists():
            row["speaker_embedding_model"] = backend_label
            row["speaker_similarity"] = "missing_reference_audio"
            continue
        if not output_path.exists():
            row["failure_type"] = row.get("failure_type") or "model_error"
            row["failure_reason"] = f"Audio file missing during speaker evaluation: {output_path}"
            continue

        if backend is None:
            backend = SpeechBrainSpeakerEmbedding(source=model_source, savedir=savedir, device=device)
            backend_label = backend.model_label

        reference_embedding = backend.embed(reference_path)
        output_embedding = backend.embed(output_path)
        similarity = cosine_similarity(reference_embedding.vector, output_embedding.vector)

        row["speaker_embedding_model"] = backend_label
        row["speaker_similarity"] = round(similarity, 6)
        similarities.append(
            {
                "sample_id": row.get("sample_id"),
                "language": row.get("language"),
                "model_id": row.get("model_id"),
                "reference_audio": str(reference_path),
                "output_audio": str(output_path),
                "speaker_embedding_model": backend_label,
                "speaker_similarity": round(similarity, 6),
            }
        )

    write_benchmark_csv(benchmark_path, rows)
    write_json(run_path / "speaker_similarity.json", similarities)
    return benchmark_path



def evaluate_mos(run_dir: str | Path, *, ratings_path: str | Path | None = None) -> Path:
    run_path = Path(run_dir)
    benchmark_path = run_path / "benchmark.csv"
    if not benchmark_path.exists():
        raise FileNotFoundError(f"Benchmark CSV not found: {benchmark_path}")

    ratings_file = Path(ratings_path) if ratings_path else run_path / "mos_ratings_template.csv"
    if not ratings_file.exists():
        raise FileNotFoundError(f"MOS ratings CSV not found: {ratings_file}")

    rows = _read_benchmark_csv(benchmark_path)
    ratings, invalid_rows = _read_mos_ratings(ratings_file)
    aggregations = aggregate_mos_ratings(ratings)

    for row in rows:
        if row.get("status") != "success":
            continue
        aggregation = aggregations.get(row.get("sample_id", ""))
        if aggregation is None or aggregation.mos is None:
            row["mos"] = "pending_human_eval"
            continue
        row["mos"] = round(aggregation.mos, 6)

    summary = {
        "ratings_file": str(ratings_file),
        "valid_rating_count": len(ratings),
        "invalid_rating_count": len(invalid_rows),
        "invalid_rows": invalid_rows,
        "samples": [
            {
                "sample_id": aggregation.sample_id,
                "mos": round(aggregation.mos, 6) if aggregation.mos is not None else None,
                "rating_count": aggregation.rating_count,
                "score_std": round(aggregation.score_std, 6) if aggregation.score_std is not None else None,
                "ratings": [
                    {
                        "listener_id": rating.listener_id,
                        "score": rating.score,
                        "same_speaker_ab": rating.same_speaker_ab,
                        "notes": rating.notes,
                    }
                    for rating in aggregation.ratings
                ],
            }
            for aggregation in aggregations.values()
        ],
    }

    write_benchmark_csv(benchmark_path, rows)
    write_json(run_path / "mos_summary.json", summary)
    return benchmark_path


def _read_mos_ratings(path: Path) -> tuple[list[MOSRating], list[dict[str, Any]]]:
    ratings: list[MOSRating] = []
    invalid_rows: list[dict[str, Any]] = []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for line_number, row in enumerate(reader, start=2):
            sample_id = (row.get("sample_id") or "").strip()
            listener_id = (row.get("listener_id") or "").strip()
            raw_score = row.get("score_1_to_5") or row.get("score") or ""
            if not sample_id and not raw_score.strip():
                continue
            if not sample_id:
                invalid_rows.append({"line_number": line_number, "reason": "missing sample_id", "row": row})
                continue
            try:
                score = parse_mos_score(raw_score)
            except ValueError as exc:
                invalid_rows.append({"line_number": line_number, "sample_id": sample_id, "reason": str(exc), "row": row})
                continue
            if score is None:
                continue
            ratings.append(
                MOSRating(
                    sample_id=sample_id,
                    listener_id=listener_id,
                    score=score,
                    same_speaker_ab=(row.get("same_speaker_ab") or "").strip(),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    return ratings, invalid_rows

