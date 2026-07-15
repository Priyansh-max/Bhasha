# Multilingual Candidate Dry Run

This is a lightweight local dry-run of the assignment candidate suite.

Command:

```bash
.venv\Scripts\python -m bhasha run --suite configs\suites\multilingual_tts_takehome_v1.json --include-disabled
```

This did not install or execute heavy TTS models. It records which configured candidates are unavailable locally because their adapters are pending and which language/model combinations are unsupported by configuration.

Purpose:

- Preserve honest local failure/deferred evidence.
- Avoid stressing the laptop.
- Keep the assignment reproducible without fabricating model metrics.
