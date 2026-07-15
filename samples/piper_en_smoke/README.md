# Piper English Smoke Evidence

This folder contains the small tracked evidence package from the first real local TTS run.

Source run:

```text
outputs/runs/20260715T100951Z_piper_en_smoke
```

Contents:

- `audio/`: real generated Piper WAV clips.
- `benchmark.csv`: measured latency, duration, RTF, ASR WER/CER, MOS status, speaker-similarity status.
- `transcripts.json`: faster-whisper tiny CPU transcript evidence.
- `speaker_similarity.json`: empty for Piper because Piper is not a voice-cloning model.
- `results.md`: generated summary report for the run.

These are local validation numbers, not final cross-model leaderboard results.
