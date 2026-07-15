from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_suite
from .runner import run_suite


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="bhasha", description="Run reproducible multilingual TTS benchmarks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a benchmark suite.")
    run_parser.add_argument("--suite", required=True, help="Path to a suite TOML file.")
    run_parser.add_argument("--model", help="Optional model id filter.")
    run_parser.add_argument("--language", help="Optional language id filter.")
    run_parser.add_argument(
        "--include-disabled",
        action="store_true",
        help="Include disabled model configs. Missing adapters will be recorded as skipped.",
    )

    inspect_parser = subparsers.add_parser("inspect", help="Print a summary of a suite config.")
    inspect_parser.add_argument("--suite", required=True, help="Path to a suite TOML file.")

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

    raise SystemExit(f"Unknown command: {args.command}")
