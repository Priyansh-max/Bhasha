# Local CPU Example Report

## Summary

This example shows a conservative Bhasha run on a local CPU-oriented environment. It demonstrates the full artifact flow with a lightweight Piper baseline and records heavier multilingual candidates as skipped/deferred when their optional dependencies are not installed.

This is an example evidence package, not a global leaderboard.

## What Was Exercised

- Config-driven benchmark runner.
- Piper CLI adapter with real generated English audio.
- Latency, duration, and RTF measurement.
- ASR round-trip WER/CER using faster-whisper tiny CPU.
- Speaker similarity framework, marked `not_applicable` for Piper.
- MOS workflow, left `pending_human_eval` because no listener ratings were entered.
- Candidate dry-run for optional heavyweight adapters.

## Real Local TTS Evidence

Tracked evidence package:

```text
samples/piper_en_smoke/
```

Model:

```text
Piper en_US lessac medium
```

Measured local results:

| Prompt | Duration | Generation Time | RTF | WER | CER | MOS | Speaker Similarity |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| en_piper_001 | 3.494603 | 1.838535 | 0.526107 | 0.083333 | 0.018182 | pending_human_eval | not_applicable |
| en_piper_002 | 3.552653 | 1.781665 | 0.501503 | 0.2 | 0.0 | pending_human_eval | not_applicable |

Notes:

- Piper is not a voice-cloning model, so speaker similarity is `not_applicable`.
- MOS is pending because no real listener ratings were entered.
- WER/CER used `faster-whisper:tiny:cpu:int8`, which is suitable for smoke tests but not a final high-accuracy ASR setting.
- The second prompt shows a normalization issue: `9:30` vs `930` raises WER while CER remains 0.0.

## Candidate Dry Run

Tracked dry-run evidence:

```text
samples/multilingual_candidate_dry_run/
```

This run did not execute heavyweight models. It verifies adapter registration and records dependency/configuration gaps cleanly.

## Current Local Baseline

English local CPU baseline:

```text
Piper en_US lessac medium
```

Reason:

- Runs locally on CPU.
- Produces real audio.
- RTF around 0.50-0.53 in the measured evidence run.
- WER/CER can be evaluated automatically.

Limitations:

- Not a voice-cloning model.
- Naturalness may be lower than newer heavyweight models.
- Only English was generated in this local CPU example.

## No Global Winner Claimed

A fair multilingual leaderboard requires real generated audio and measured metrics for every compared model on a fixed hardware profile. This example does not claim winners for Arabic, Hindi, or heavyweight models.

## Recommended Full Benchmark Run

Use one fixed GPU environment and run all comparable candidates there. Do not mix local and cloud speed metrics.

Suggested candidate set:

- English: Chatterbox/Turbo, Fish Speech, XTTS-v2, Piper baseline.
- Arabic: XTTS-v2, Fish Speech, MMS-TTS or Arabic fine-tune.
- Hindi: Indic Parler-TTS, XTTS-v2, MMS-TTS/Indic-TTS.

Final ASR should use a stronger model such as faster-whisper large-v3 if hardware allows.

## Known Limitations

- Heavy adapters require separate dependency installation.
- No consented/openly licensed reference voice clip is included by default.
- No real MOS ratings are included by default.
- Round-trip WER depends on ASR quality and normalization, so it is a proxy metric.
