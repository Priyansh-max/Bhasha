# Bhasha Local Assignment Report

## Executive Summary

Bhasha is a reproducible multilingual TTS benchmark framework built for the English/Arabic/Hindi take-home assignment. The local-safe version intentionally avoids heavy model installs and cloud GPU cost. It includes a real CPU-friendly English TTS baseline, full metric plumbing, and honest skipped/unsupported evidence for heavier candidates.

No Arabic or Hindi winner is claimed from local generation because no Arabic/Hindi TTS model was run on this laptop. This is intentional: reported numbers must come from real runs.

## What Was Built

- Config-driven benchmark runner.
- Adapter interface for TTS models.
- Piper CLI adapter as the first real TTS baseline.
- Latency, audio duration, and RTF measurement.
- ASR round-trip WER/CER using faster-whisper.
- Speaker similarity evaluation framework using optional SpeechBrain embeddings.
- MOS rating template and aggregation from real listener scores.
- Markdown report generator.
- Fixed English, Arabic, and Hindi assignment prompt suite.
- Reference voice metadata template with consent/license fields.
- Tracked evidence samples under `samples/`.

## Local Hardware Policy

The laptop is used only for lightweight work. Heavy TTS candidates are deferred to avoid stressing the machine. See:

```text
docs/assignment/local_compute_policy.md
```

## Real Local TTS Evidence

Tracked evidence package:

```text
samples/piper_en_smoke/
```

Model:

```text
Piper en_US lessac medium
```

Run source:

```text
outputs/runs/20260715T100951Z_piper_en_smoke
```

Measured local results:

| Prompt | Duration | Generation Time | RTF | WER | CER | MOS | Speaker Similarity |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| en_piper_001 | 3.494603 | 1.838535 | 0.526107 | 0.083333 | 0.018182 | pending_human_eval | not_applicable |
| en_piper_002 | 3.552653 | 1.781665 | 0.501503 | 0.2 | 0.0 | pending_human_eval | not_applicable |

Notes:

- Piper is not a voice-cloning model, so speaker similarity is `not_applicable`.
- MOS is pending because no real listener ratings were entered.
- WER/CER used `faster-whisper:tiny:cpu:int8`, which is lightweight and not the final recommended ASR model.
- The second prompt shows a normalization issue: `9:30` vs `930` raises WER while CER remains 0.0.

## Candidate Dry Run

Tracked dry-run evidence:

```text
samples/multilingual_candidate_dry_run/
```

This run did not execute heavy models. It records local availability status for configured candidates:

```text
33 skipped
21 unsupported
```

Skipped means adapter/model execution was not available locally. Unsupported means the model config does not claim that language.

## Candidate Matrix

See:

```text
docs/assignment/candidate_matrix.md
```

## Current Best Local Pipeline

English local-safe baseline:

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
- Naturalness likely below modern heavyweight models.
- Only English was run locally.

## No Claimed Winner For Arabic/Hindi

Arabic and Hindi candidate models are configured but not run locally. A fair winner requires actual generated audio and measured metrics on a fixed hardware profile. The framework is ready for those runs, but this local-safe version does not fabricate results.

## Recommended Next Run If Compute Becomes Available

Use one fixed GPU environment and run all comparable candidates there. Do not mix local and cloud speed metrics.

Suggested final candidate set:

- English: Chatterbox/Turbo, Fish Speech, XTTS-v2, Piper baseline.
- Arabic: XTTS-v2, Fish Speech, MMS-TTS or Arabic fine-tune.
- Hindi: Indic Parler-TTS, XTTS-v2, MMS-TTS/Indic-TTS.

Final ASR should use a stronger model such as faster-whisper large-v3 if hardware allows.

## Honest Failure Modes

- Local laptop is not suitable for heavyweight model comparison.
- No consented/openly licensed reference voice clip has been recorded yet.
- No real MOS ratings have been collected yet.
- Heavy candidates are configured but deferred.
- Round-trip WER depends on ASR quality and text normalization, so it is a proxy, not pure TTS correctness.
