# ASR Round-Trip WER/CER

Bhasha can estimate intelligibility by transcribing generated audio and comparing the ASR transcript to the original input text.

```text
input text -> TTS audio -> ASR transcript -> WER/CER
```

## What It Measures

- **WER**: word-level difference between input text and ASR transcript.
- **CER**: character-level difference between input text and ASR transcript.

These are proxy metrics. They depend on TTS clarity, ASR quality, text normalization, and language/script behavior.

## Command

```bash
python -m bhasha eval-asr --run-dir outputs/runs/<run_id> --model-size tiny --device cpu --compute-type int8
```

For final benchmark runs, use the same ASR model and compute settings across comparable runs.

## Outputs

- Updates `benchmark.csv`: `asr_model`, `asr_transcript`, `wer`, `cer`.
- Writes `transcripts.json` with normalized text and transcript evidence.

## Caveat

Numbers and punctuation can affect WER strongly. For example, input `9:30` may be transcribed as `930`. CER helps reveal when the spoken content is mostly preserved despite word-token differences.
