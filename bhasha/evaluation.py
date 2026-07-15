from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .asr.faster_whisper_backend import FasterWhisperASR
from .reporting import BENCHMARK_FIELDS, write_benchmark_csv, write_json
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
