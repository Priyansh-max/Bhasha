# Bhasha

Bhasha is an open-source benchmark framework for evaluating text-to-speech systems across languages, models, voices, and hardware profiles.

It is built around evidence, not claims: every run writes generated audio, measured timing, transcripts, metric tables, human-rating templates, hardware metadata, and failure records. If a model cannot run, Bhasha records why instead of hiding it.

## What Bhasha Measures

Bhasha is designed to evaluate TTS systems on:

| Metric | What It Answers | Output Field |
| --- | --- | --- |
| Generation latency | How long did synthesis take? | `generation_time_seconds`, `time_to_first_audio_seconds` |
| Audio duration | How long is the produced clip? | `audio_duration_seconds` |
| Real-Time Factor | Is generation faster than playback? | `rtf` |
| Round-trip WER | Can ASR recover the intended words? | `wer` |
| Round-trip CER | Can ASR recover the intended characters? | `cer` |
| Speaker similarity | Does cloned speech match the reference speaker? | `speaker_similarity` |
| MOS naturalness | How natural does the audio sound to listeners? | `mos` |
| Failure status | Did the model run, skip, fail, or lack support? | `status`, `failure_type`, `failure_reason` |

Round-trip WER/CER are ASR-based intelligibility proxies, not perfect TTS correctness metrics. MOS comes only from real listener ratings. Speed metrics should only be compared within the same hardware profile.

## Core Concepts

- **Suite**: a benchmark definition with languages, prompts, models, and settings.
- **Adapter**: a small integration layer that lets Bhasha call a TTS engine or model.
- **Run**: one execution of a suite on one machine/hardware profile.
- **Artifact**: generated audio, CSV metrics, metadata, reports, transcripts, and failure logs.

## Quick Start

Install the lightweight Piper baseline:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements/piper.txt
.venv\Scripts\python scripts\download_piper_voice.py
```

Run a real local TTS benchmark:

```bash
$env:PATH = (Resolve-Path '.venv\Scripts').Path + ';' + $env:PATH
.venv\Scripts\python -m bhasha run --suite configs\suites\piper_en_smoke.json
```

Outputs are written to:

```text
outputs/runs/<run_id>/
```

Generate a Markdown report:

```bash
.venv\Scripts\python -m bhasha generate-report --run-dir outputs\runs\<run_id>
```

## Common Commands

Inspect a suite:

```bash
python -m bhasha inspect --suite configs/suites/multilingual_tts_core_v1.json
```

Run a suite:

```bash
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --include-disabled
```

Evaluate ASR round-trip WER/CER:

```bash
python -m bhasha eval-asr --run-dir outputs/runs/<run_id> --model-size tiny --device cpu --compute-type int8
```

Evaluate speaker similarity:

```bash
python -m bhasha eval-speaker --run-dir outputs/runs/<run_id> --device cpu
```

Aggregate real listener MOS ratings:

```bash
python -m bhasha eval-mos --run-dir outputs/runs/<run_id>
```

## Candidate Adapters

Bhasha includes optional adapter entry points for:

- Piper
- XTTS-v2
- Chatterbox
- Fish Speech via external command
- CosyVoice2 via external command
- Indic Parler-TTS
- Hugging Face VITS / MMS-TTS

Heavy adapters are not installed by default. Install one dependency file at a time, preferably on a GPU notebook or a fixed cloud/GPU machine.

See:

```text
docs/model_adapters.md
docs/kaggle_gpu_runbook.md
```

## Example Evidence

Tracked example outputs are under:

```text
samples/piper_en_smoke/
samples/multilingual_candidate_dry_run/
```

The local CPU example is documented in:

```text
examples/local_cpu/report.md
examples/local_cpu/compute_policy.md
examples/local_cpu/candidate_matrix.md
```

These examples show how Bhasha records real measurements and honest skipped/deferred models. They are not a global leaderboard.

## Add A New Model

1. Add an adapter under `bhasha/adapters/`.
2. Register it in `bhasha/adapters/registry.py`.
3. Add a model entry to a suite JSON file.
4. Run the suite.
5. Evaluate ASR, speaker similarity, and MOS as applicable.
6. Generate a report.

A model adapter should return structured success, skipped, failed, or unsupported results. Missing dependencies should be recorded as `skipped` with a clear reason.

## Benchmark Rules

1. Do not fabricate metrics.
2. Save generated audio and benchmark rows.
3. Record hardware and dependency failures.
4. Compare speed only within the same hardware profile.
5. Keep MOS separate from automatic metrics.
6. Use consented or openly licensed reference clips for voice cloning.
7. Report unsupported languages explicitly.
