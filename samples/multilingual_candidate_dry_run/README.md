# Multilingual Candidate Dry Run

This is a lightweight local dry-run of the core multilingual candidate suite.

Command:

```bash
.venv\Scripts\python -m bhasha run --suite configs\suites\multilingual_tts_core_v1.json --include-disabled
```

This does not install or execute heavyweight TTS models. It verifies that optional adapters are registered and records dependency/configuration gaps cleanly.

Purpose:

- Preserve honest local failure/deferred evidence.
- Avoid stressing local hardware.
- Confirm adapter entry points for XTTS-v2, Chatterbox, Fish Speech, CosyVoice2, Indic Parler-TTS, and MMS-TTS.
- Keep benchmark behavior reproducible without fabricating model metrics.
