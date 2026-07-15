from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any


BENCHMARK_FIELDS = [
    "run_id",
    "sample_id",
    "suite_id",
    "language",
    "model_id",
    "prompt_id",
    "input_text",
    "reference_audio",
    "output_audio",
    "generation_time_seconds",
    "audio_duration_seconds",
    "rtf",
    "latency_type",
    "time_to_first_audio_seconds",
    "asr_model",
    "asr_transcript",
    "wer",
    "cer",
    "speaker_embedding_model",
    "speaker_similarity",
    "mos",
    "status",
    "failure_type",
    "failure_reason",
]


def write_benchmark_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=BENCHMARK_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in BENCHMARK_FIELDS})


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(_jsonable(data), handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_mos_template(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["sample_id", "listener_id", "score_1_to_5", "same_speaker_ab", "notes"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            if row.get("status") == "success":
                writer.writerow(
                    {
                        "sample_id": row["sample_id"],
                        "listener_id": "",
                        "score_1_to_5": "",
                        "same_speaker_ab": "",
                        "notes": "",
                    }
                )


def write_audio_index(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = ["# Audio Samples", ""]
    for row in rows:
        if row.get("status") != "success":
            continue
        lines.extend(
            [
                f"## {row['sample_id']}",
                "",
                f"- Language: `{row['language']}`",
                f"- Model: `{row['model_id']}`",
                f"- Prompt: `{row['prompt_id']}`",
                f"- Text: {row['input_text']}",
                f"- Audio: `{row['output_audio']}`",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def _jsonable(data: Any) -> Any:
    if hasattr(data, "to_dict"):
        return data.to_dict()
    if hasattr(data, "__dataclass_fields__"):
        return _jsonable(asdict(data))
    if isinstance(data, Path):
        return str(data)
    if isinstance(data, list):
        return [_jsonable(item) for item in data]
    if isinstance(data, dict):
        return {key: _jsonable(value) for key, value in data.items()}
    return data


