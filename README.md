# Bhasha

Bhasha is a reproducible multilingual text-to-speech benchmark framework. The first target suite is an AI Engineer take-home evaluation for English, Arabic, and Hindi TTS pipelines, but the framework is designed so future models and languages can be added through adapters and config files.

The project is assignment-first: it records real generated audio, measured metrics, hardware details, failures, and human-listening evidence. It must not fabricate MOS or any other metric.

## Current Milestone

Milestone 1 is a benchmark skeleton:

- Suite configuration files.
- CLI runner.
- Dummy model adapter that generates a valid WAV tone.
- Structured output directory.
- `benchmark.csv`, `metadata.json`, `failures.json`, `audio_samples_index.md`, and `mos_ratings_template.csv`.

The dummy adapter is not a TTS model. It exists only to verify the benchmark mechanics before installing heavy models.

## Quick Start

```bash
python -m bhasha run --suite configs/suites/smoke_test.json
```

Outputs are written to:

```text
outputs/runs/<run_id>/
```

## Benchmark Rules

1. Compare speed only within the same hardware profile.
2. Use the same prompts, reference clips, and settings for all comparable models.
3. Save every generated audio file.
4. Record failed and skipped models honestly.
5. Do not report MOS until real listeners have rated clips.
6. Keep model versions, hardware, parameters, and commands in the report.

## Assignment Metrics

Bhasha is planned to evaluate:

- MOS naturalness score from real listeners.
- Speaker embedding cosine similarity for voice cloning.
- Latency to first audio or full batch clip.
- Real-Time Factor: generation time divided by audio duration.
- Round-trip WER and CER using ASR.
- Cross-language robustness across English, Arabic, and Hindi.

## Compute Plan

Development can happen locally. Heavy benchmark runs should happen on one fixed GPU environment. Results from different hardware profiles must be reported separately.

## Next Milestones

1. Add the first real local TTS adapter.
2. Add audio duration and stronger latency instrumentation.
3. Add ASR WER/CER evaluation.
4. Add speaker similarity for cloning-capable models.
5. Add the English, Arabic, and Hindi take-home suite with real model candidates.


## Piper Baseline

Piper is the first real local TTS baseline. It is CPU-friendly and useful for validating Bhasha with actual generated speech before moving to heavyweight multilingual/cloning models.

Setup:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements/piper.txt
.venv\Scripts\python scripts\download_piper_voice.py
```

Run:

```bash
$env:PATH = (Resolve-Path '.venv\Scripts').Path + ';' + $env:PATH
.venv\Scripts\python -m bhasha run --suite configs\suites\piper_en_smoke.json
```

The current Piper adapter invokes the `piper` CLI per sample, so measured latency includes process/model startup. Later benchmark stages should separate cold-start timing from warm generation timing.

## ASR Round-Trip Evaluation

Bhasha computes intelligibility by transcribing generated audio and comparing the ASR transcript to the original input text.

Install the optional ASR dependency:

```bash
.venv\Scripts\python -m pip install -r requirements/asr.txt
```

Evaluate an existing run:

```bash
.venv\Scripts\python -m bhasha eval-asr --run-dir outputs\runs\<run_id> --model-size tiny --device cpu --compute-type int8
```

This updates `benchmark.csv` with:

- `asr_model`
- `asr_transcript`
- `wer`
- `cer`

It also writes `transcripts.json` with normalized text and transcript details. For final results, use the same ASR model and hardware policy across comparable runs.

WER note: numbers and punctuation can affect word-level scoring. Bhasha also reports CER so cases like `9:30` versus `930` are easier to interpret.
