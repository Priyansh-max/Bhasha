from __future__ import annotations

import argparse
from pathlib import Path

from .asr import ASRBackendError
from .config import load_suite
from .evaluation import evaluate_asr, evaluate_mos, evaluate_speaker_similarity
from .runner import run_suite
from .speaker import SpeakerBackendError


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="bhasha", description="Run reproducible multilingual TTS benchmarks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a benchmark suite.")
    run_parser.add_argument("--suite", required=True, help="Path to a suite JSON/TOML file.")
    run_parser.add_argument("--model", help="Optional model id filter.")
    run_parser.add_argument("--language", help="Optional language id filter.")
    run_parser.add_argument(
        "--include-disabled",
        action="store_true",
        help="Include disabled model configs. Missing adapters will be recorded as skipped.",
    )

    inspect_parser = subparsers.add_parser("inspect", help="Print a summary of a suite config.")
    inspect_parser.add_argument("--suite", required=True, help="Path to a suite JSON/TOML file.")

    asr_parser = subparsers.add_parser("eval-asr", help="Run ASR round-trip WER/CER evaluation for a completed run.")
    asr_parser.add_argument("--run-dir", required=True, help="Path to an outputs/runs/<run_id> directory.")
    asr_parser.add_argument("--model-size", default="tiny", help="faster-whisper model size or local model path.")
    asr_parser.add_argument("--device", default="cpu", help="ASR device, for example cpu or cuda.")
    asr_parser.add_argument("--compute-type", default="int8", help="faster-whisper compute type, for example int8 or float16.")

    speaker_parser = subparsers.add_parser("eval-speaker", help="Run speaker embedding cosine similarity evaluation for a completed run.")
    speaker_parser.add_argument("--run-dir", required=True, help="Path to an outputs/runs/<run_id> directory.")
    speaker_parser.add_argument("--model-source", default="speechbrain/spkrec-ecapa-voxceleb", help="SpeechBrain speaker model source or local path.")
    speaker_parser.add_argument("--savedir", default="models/speaker/speechbrain-spkrec-ecapa-voxceleb", help="Local directory for downloaded speaker model files.")
    speaker_parser.add_argument("--device", default="cpu", help="Speaker embedding device, for example cpu or cuda.")

    mos_parser = subparsers.add_parser("eval-mos", help="Aggregate real listener MOS ratings for a completed run.")
    mos_parser.add_argument("--run-dir", required=True, help="Path to an outputs/runs/<run_id> directory.")
    mos_parser.add_argument("--ratings", help="Optional path to filled MOS ratings CSV. Defaults to mos_ratings_template.csv in the run directory.")

    args = parser.parse_args(argv)

    if args.command == "run":
        suite = load_suite(args.suite)
        run_dir = run_suite(
            suite,
            model_filter=args.model,
            language_filter=args.language,
            include_disabled=args.include_disabled,
        )
        print(f"Run complete: {Path(run_dir).resolve()}")
        return

    if args.command == "inspect":
        suite = load_suite(args.suite)
        print(f"Suite: {suite.suite_id} - {suite.name}")
        print(f"Languages: {', '.join(language.id for language in suite.languages)}")
        print(f"Models: {', '.join(model.id for model in suite.models)}")
        print(f"Prompts: {len(suite.prompts)}")
        return

    if args.command == "eval-asr":
        try:
            benchmark_path = evaluate_asr(
                args.run_dir,
                model_size=args.model_size,
                device=args.device,
                compute_type=args.compute_type,
            )
        except ASRBackendError as exc:
            raise SystemExit(str(exc)) from exc
        print(f"ASR evaluation complete: {Path(benchmark_path).resolve()}")
        return

    if args.command == "eval-speaker":
        try:
            benchmark_path = evaluate_speaker_similarity(
                args.run_dir,
                model_source=args.model_source,
                savedir=args.savedir,
                device=args.device,
            )
        except SpeakerBackendError as exc:
            raise SystemExit(str(exc)) from exc
        print(f"Speaker evaluation complete: {Path(benchmark_path).resolve()}")
        return

    if args.command == "eval-mos":
        benchmark_path = evaluate_mos(args.run_dir, ratings_path=args.ratings)
        print(f"MOS evaluation complete: {Path(benchmark_path).resolve()}")
        return

    raise SystemExit(f"Unknown command: {args.command}")
