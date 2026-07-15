# Milestone 3: ASR Round-Trip Evaluation

Bhasha now supports round-trip intelligibility evaluation:

```text
input text -> TTS audio -> ASR transcript -> WER/CER
```

## Implemented

- `bhasha.text_metrics.normalize_text`
- `bhasha.text_metrics.word_error_rate`
- `bhasha.text_metrics.character_error_rate`
- Optional `faster-whisper` ASR backend
- `bhasha eval-asr` CLI command
- `transcripts.json` evidence output
- `benchmark.csv` update with `asr_model`, `asr_transcript`, `wer`, and `cer`

## Command

```bash
.venv\Scripts\python -m bhasha eval-asr --run-dir outputs\runs\<run_id> --model-size tiny --device cpu --compute-type int8
```

## Local Verification Run

Run evaluated locally:

```text
outputs/runs/20260715T100951Z_piper_en_smoke
```

ASR backend:

```text
faster-whisper:tiny:cpu:int8
```

Observed rows:

```text
en_piper_001: WER 0.083333, CER 0.018182
en_piper_002: WER 0.2, CER 0.0
```

These are not final assignment numbers. They are local framework-validation numbers from the Piper baseline.

## Normalization Caveat

Numbers and punctuation can affect WER strongly. For example, the input `9:30` normalizes to `9 30`, while ASR may output `930`. That can increase WER even when the spoken content is understandable. CER is included to make this visible, especially for multilingual scripts.
