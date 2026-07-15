# Multilingual Candidate Dry Run

This is a lightweight local dry-run of the assignment candidate suite.

Command:

```bash
.venv\Scripts\python -m bhasha run --suite configs\suites\multilingual_tts_takehome_v1.json --include-disabled
```

This did not install or execute heavy TTS models. It verifies that the optional adapters are registered and records dependency/configuration gaps cleanly.

Purpose:

- Preserve honest local failure/deferred evidence.
- Avoid stressing the laptop.
- Confirm the code has adapter entry points for XTTS-v2, Chatterbox, Fish Speech, CosyVoice2, Indic Parler-TTS, and MMS-TTS.
- Keep the assignment reproducible without fabricating model metrics.
