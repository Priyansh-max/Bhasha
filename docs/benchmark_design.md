# Bhasha Benchmark Design

## Purpose

Bhasha compares TTS systems under controlled conditions. A benchmark run should answer:

> Given a language, model, prompt, hardware profile, and optional reference voice, how good, fast, reproducible, and reliable is the generated speech?

## Core Objects

### Suite

A suite defines the benchmark task. It contains languages, prompts, candidate models, and run settings.

### Language

A language entry stores the display name, BCP-47-ish language code, script, and ASR language hint.

### Prompt

A prompt is a fixed test sentence. Prompts should cover simple speech, numbers, names, punctuation, and longer phrasing.

### Model

A model entry describes an adapter, source, license, supported languages, cloning support, and model parameters.

### Run

A run is one execution of a suite on a specific machine. Bhasha records the hardware profile so results can be grouped fairly.

## Result Schema

Each generated row should contain:

```text
run_id
sample_id
suite_id
language
model_id
prompt_id
input_text
reference_audio
output_audio
generation_time_seconds
audio_duration_seconds
rtf
latency_type
time_to_first_audio_seconds
asr_model
asr_transcript
wer
cer
speaker_embedding_model
speaker_similarity
mos
status
failure_type
failure_reason
```

## Status Values

```text
success
skipped
failed
unsupported
not_applicable
```

## Failure Types

```text
hardware_limit
dependency_error
model_error
unsupported_language
unsupported_task
timeout
unknown
```

## Fairness Rules

- Speed metrics are comparable only within the same hardware profile.
- Quality metrics should use identical prompts and decoding parameters.
- Different hardware profiles must be reported as separate tables.
- A model that cannot run on available hardware is not a bad model; it is a failed or unsupported run for that hardware profile.

## MOS Policy

MOS is a human score. Bhasha can create rating templates and aggregate ratings, but must not invent MOS values. Until ratings exist, MOS is `pending_human_eval`.
