# Local Compute Policy

This project is intentionally local-first for the learning version of the assignment.

## Decision

No cloud GPU is required for the current submitted evidence package. Heavy models are not installed or run on the laptop.

## Why

The local machine is older and has limited RAM/VRAM. Running large multilingual voice-cloning models locally may cause long runtimes, out-of-memory failures, thermal stress, or dependency conflicts. Since the assignment value is uncertain, Bhasha prioritizes a reproducible framework, one lightweight real TTS baseline, and honest failure/deferred status for heavier candidates.

## What Is Safe Locally

- Project development
- Config validation
- Piper CPU baseline
- Tiny faster-whisper ASR evaluation
- CSV/Markdown report generation
- Failure recording for unavailable adapters/models

## What Is Deferred

- Fish Speech
- CosyVoice2
- Chatterbox full comparison
- XTTS-v2 multilingual cloning runs
- Whisper large-v3 final ASR scoring
- SpeechBrain speaker scoring on large batches

These can be run later on one fixed GPU profile. Speed metrics from cloud and local hardware must not be mixed.
