# Bhasha TODO

The priority is the AI Engineer take-home assignment first. Bhasha should remain reusable, but we will avoid building unnecessary product features.

## Milestone 1: Benchmark Skeleton

- [x] Define assignment-first scope.
- [x] Create benchmark schema for suites, languages, models, prompts, runs, metrics, and failures.
- [x] Add CLI entrypoint: `python -m bhasha`.
- [x] Add dummy adapter for local smoke tests.
- [x] Write structured run artifacts: audio, benchmark CSV, metadata, failures, MOS template, audio index.
- [x] Verify smoke suite runs on local Python 3.10.

## Milestone 2: First Real Audio

- [x] Choose first lightweight real TTS model for local or notebook testing.
- [x] Add first real TTS adapter.
- [x] Generate real audio samples.
- [x] Record install steps and model version.

## Milestone 3: Objective Metrics

- [x] Add robust WAV audio duration extraction.
- [x] Add WER/CER metric code.
- [x] Add ASR adapter using faster-whisper or another documented ASR backend.
- [x] Add speaker embedding cosine similarity for cloning-capable models.
- [x] Add MOS aggregation from real listener ratings.

## Milestone 4: Take-Home Suite

- [x] Finalize English, Arabic, and Hindi prompt sets.
- [x] Add reference voice clip metadata and licensing notes.
- [x] Test 2-3 candidate model configs per language where hardware allows; heavy inference deferred locally.
- [x] Record failed, skipped, unsupported, or out-of-memory runs honestly.

## Milestone 5: Submission Package

- [x] Generate local evidence `benchmark.csv` files.
- [x] Generate results report with comparison tables.
- [x] Pick only measured local English baseline; do not claim Arabic/Hindi winners without runs.
- [x] Document model versions, hardware policy, parameters, reproduction steps, and failure modes.
- [x] Package real audio samples and reference clip metadata.






