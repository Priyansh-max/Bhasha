from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any


def generate_run_report(run_dir: str | Path, *, output_path: str | Path | None = None) -> Path:
    run_path = Path(run_dir)
    benchmark_path = run_path / "benchmark.csv"
    if not benchmark_path.exists():
        raise FileNotFoundError(f"Benchmark CSV not found: {benchmark_path}")

    rows = _read_rows(benchmark_path)
    destination = Path(output_path) if output_path else run_path / "results.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(_render_report(run_path, rows), encoding="utf-8")
    return destination


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _render_report(run_path: Path, rows: list[dict[str, str]]) -> str:
    status_counts = Counter(row.get("status", "unknown") or "unknown" for row in rows)
    languages = sorted({row.get("language", "") for row in rows if row.get("language")})
    models = sorted({row.get("model_id", "") for row in rows if row.get("model_id")})

    lines = [
        "# Bhasha Run Report",
        "",
        f"Run directory: `{run_path}`",
        "",
        "## Scope",
        "",
        f"- Languages: {', '.join(languages) if languages else 'none'}",
        f"- Models: {', '.join(models) if models else 'none'}",
        f"- Samples: {len(rows)}",
        "",
        "## Status Counts",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]

    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")

    lines.extend(
        [
            "",
            "## Metrics",
            "",
            "| Sample | Lang | Model | Status | Duration | Gen Time | RTF | WER | CER | Speaker Sim | MOS |",
            "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(row.get("sample_id")),
                    _cell(row.get("language")),
                    _cell(row.get("model_id")),
                    _cell(row.get("status")),
                    _cell(row.get("audio_duration_seconds")),
                    _cell(row.get("generation_time_seconds")),
                    _cell(row.get("rtf")),
                    _cell(row.get("wer")),
                    _cell(row.get("cer")),
                    _cell(row.get("speaker_similarity")),
                    _cell(row.get("mos")),
                ]
            )
            + " |"
        )

    failures = [row for row in rows if row.get("status") != "success" or row.get("failure_reason")]
    if failures:
        lines.extend(["", "## Failures And Skips", ""])
        for row in failures:
            lines.append(
                f"- `{row.get('sample_id')}`: {row.get('status')} / {row.get('failure_type') or 'n/a'} - {row.get('failure_reason') or 'no reason recorded'}"
            )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- MOS is reported only when real listener ratings are provided.",
            "- WER/CER are round-trip ASR proxy metrics, not pure TTS quality scores.",
            "- Speed metrics should only be compared within the same hardware profile.",
        ]
    )
    return "\n".join(lines) + "\n"


def _cell(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|")
