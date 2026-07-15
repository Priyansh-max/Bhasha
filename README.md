<div align="center">

# 🔊 Bhasha

### A reproducible benchmark framework for multilingual Text-to-Speech systems.

**Compare TTS models across languages, voices, speed, intelligibility, cloning similarity, and human naturalness ratings.**

<em>Bhasha means language. This project turns TTS evaluation into repeatable evidence: generated audio, benchmark tables, transcripts, metadata, failures, and reports.</em>

<br />

<a href="#quick-start"><strong>⚡ Get Started</strong></a>

<br />
<br />

![version](https://img.shields.io/badge/version-0.1.0-7ED321?style=flat-square)
![license](https://img.shields.io/badge/license-PolyForm%20Noncommercial-7ED321?style=flat-square)
![python](https://img.shields.io/badge/python-3.10%2B-111827?style=flat-square&logo=python)
![domain](https://img.shields.io/badge/domain-TTS%20Benchmark-111827?style=flat-square)
![platform](https://img.shields.io/badge/platform-Local%20%7C%20GPU%20Notebook-111827?style=flat-square)

![Piper](https://img.shields.io/badge/Piper-baseline-111827?style=flat-square)
![XTTS](https://img.shields.io/badge/XTTS--v2-adapter-111827?style=flat-square)
![Chatterbox](https://img.shields.io/badge/Chatterbox-adapter-111827?style=flat-square)
![MMS](https://img.shields.io/badge/MMS--TTS-adapter-111827?style=flat-square)
![Indic](https://img.shields.io/badge/Indic%20Parler-adapter-111827?style=flat-square)

</div>

---

## Overview

Bhasha is a benchmark framework for evaluating Text-to-Speech models under controlled, reproducible conditions.

It is designed for people who want to answer questions like:

- Which TTS model sounds most natural for a language?
- Which model is fastest on a given hardware profile?
- Does a voice-cloning model preserve the reference speaker?
- Does generated speech remain intelligible after ASR transcription?
- Which models fail because of dependencies, memory, unsupported languages, or missing reference clips?

Bhasha does not hide failures and does not fabricate metrics. Every run produces auditable artifacts.

## What Bhasha Tests

| Area | Metric | What It Means | Output |
| --- | --- | --- | --- |
| Speed | Latency | Time needed to generate audio | `generation_time_seconds`, `time_to_first_audio_seconds` |
| Speed | RTF | Generation time divided by audio duration | `rtf` |
| Audio | Duration | Length of generated clip | `audio_duration_seconds` |
| Intelligibility | WER | Word Error Rate from TTS audio transcribed by ASR | `wer` |
| Intelligibility | CER | Character Error Rate from ASR transcript | `cer` |
| Voice cloning | Speaker similarity | Cosine similarity between reference and generated speaker embeddings | `speaker_similarity` |
| Naturalness | MOS | Mean Opinion Score from real human listeners | `mos` |
| Reliability | Status/failures | Whether the model succeeded, failed, skipped, or lacked language support | `status`, `failure_type`, `failure_reason` |

Important metric rules:

- WER/CER are ASR-based intelligibility proxies, not perfect TTS correctness scores.
- MOS is never automatic; it comes from real listener ratings.
- Speed metrics should only be compared within the same hardware profile.
- Speaker similarity only applies when a valid reference clip exists.

## How It Works

```text
suite config
   ↓
model adapter
   ↓
generated audio
   ↓
latency / RTF / ASR / speaker similarity / MOS aggregation
   ↓
benchmark.csv + JSON evidence + Markdown report
```

A completed run writes:

```text
outputs/runs/<run_id>/
  audio/
  benchmark.csv
  metadata.json
  failures.json
  mos_ratings_template.csv
  audio_samples_index.md
  transcripts.json              # after eval-asr
  speaker_similarity.json       # after eval-speaker
  mos_summary.json              # after eval-mos
  results.md                    # after generate-report
```

## Quick Start

Use the lightweight Piper baseline to verify Bhasha locally.

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements/piper.txt
.venv\Scripts\python scripts\download_piper_voice.py
```

Run a real TTS benchmark:

```bash
$env:PATH = (Resolve-Path '.venv\Scripts').Path + ';' + $env:PATH
.venv\Scripts\python -m bhasha run --suite configs\suites\piper_en_smoke.json
```

Generate a report:

```bash
.venv\Scripts\python -m bhasha generate-report --run-dir outputs\runs\<run_id>
```

## Benchmark A Suite

Inspect a suite:

```bash
python -m bhasha inspect --suite configs/suites/multilingual_tts_core_v1.json
```

Run a suite:

```bash
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --include-disabled
```

Run one model/language pair:

```bash
python -m bhasha run \
  --suite configs/suites/multilingual_tts_core_v1.json \
  --model xtts_v2 \
  --language en \
  --include-disabled
```

## Evaluate A Run

ASR round-trip WER/CER:

```bash
python -m bhasha eval-asr \
  --run-dir outputs/runs/<run_id> \
  --model-size tiny \
  --device cpu \
  --compute-type int8
```

Speaker similarity:

```bash
python -m bhasha eval-speaker --run-dir outputs/runs/<run_id> --device cpu
```

MOS aggregation from real listener ratings:

```bash
python -m bhasha eval-mos --run-dir outputs/runs/<run_id>
```

Markdown report:

```bash
python -m bhasha generate-report --run-dir outputs/runs/<run_id>
```

## Model Adapters

Bhasha currently includes adapter entry points for:

| Model | Adapter | Integration Type |
| --- | --- | --- |
| Piper | `piper_cli` | CLI baseline |
| XTTS-v2 | `xtts_v2` | Coqui TTS Python API |
| Chatterbox | `chatterbox` | Python API |
| Fish Speech | `fish_speech_cli` | External command hook |
| CosyVoice2 | `cosyvoice_cli` | External command hook |
| Indic Parler-TTS | `indic_parler_tts` | Python API |
| MMS-TTS / VITS | `hf_vits` | Hugging Face Transformers |

Heavy adapters are optional. Install one stack at a time, preferably on a GPU notebook or a fixed GPU machine.

See:

```text
docs/model_adapters.md
docs/kaggle_gpu_runbook.md
```

## Add A New Model

1. Create an adapter under `bhasha/adapters/`.
2. Register it in `bhasha/adapters/registry.py`.
3. Add the model to a suite JSON file.
4. Run the suite.
5. Evaluate ASR, speaker similarity, and MOS as applicable.
6. Generate a report.

Adapters should return structured results:

```text
success
skipped
failed
unsupported
```

Missing dependencies should be recorded as `skipped` with a clear reason.

## Examples

Tracked example outputs:

```text
samples/piper_en_smoke/
samples/multilingual_candidate_dry_run/
```

Local CPU example notes:

```text
examples/local_cpu/report.md
examples/local_cpu/compute_policy.md
examples/local_cpu/candidate_matrix.md
```

These examples show artifact shape and failure handling. They are not a global leaderboard.

## Benchmark Rules

1. Do not fabricate metrics.
2. Save generated audio and benchmark rows.
3. Record hardware and dependency failures.
4. Compare speed only within the same hardware profile.
5. Keep MOS separate from automatic metrics.
6. Use consented or openly licensed reference clips for voice cloning.
7. Report unsupported languages explicitly.

## License

Bhasha is source-available for non-commercial use under the PolyForm Noncommercial License 1.0.0.

Commercial use is not permitted without separate permission. See [LICENSE](LICENSE) for details.
