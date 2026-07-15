# Bhasha Roadmap

Bhasha is a multilingual TTS benchmark framework. This checklist tracks framework work and release readiness.

## Completed

- [x] Config-driven benchmark runner.
- [x] TTS adapter interface and registry.
- [x] Structured artifacts: audio, benchmark CSV, metadata, failures, MOS template, reports.
- [x] Piper CLI baseline adapter.
- [x] Optional candidate adapters for XTTS-v2, Chatterbox, Fish Speech, CosyVoice2, Indic Parler-TTS, and MMS-TTS/VITS.
- [x] Latency, audio duration, and RTF measurement.
- [x] ASR round-trip WER/CER evaluation.
- [x] Speaker embedding cosine similarity framework.
- [x] MOS rating aggregation from real listener scores.
- [x] Markdown report generator.
- [x] Local CPU example evidence package.

## Next

- [ ] Add a stable plugin-style adapter API for third-party models.
- [ ] Add a dedicated `bhasha validate-suite` command.
- [ ] Add hardware profile IDs and grouped leaderboard reports.
- [ ] Add stronger language-specific text normalization for Arabic and Hindi.
- [ ] Add warm-start timing support separate from cold-start timing.
- [ ] Add streaming time-to-first-audio support for streaming models.
- [ ] Add CI tests for config loading and report generation.
- [ ] Run full model comparisons on one fixed GPU profile.

