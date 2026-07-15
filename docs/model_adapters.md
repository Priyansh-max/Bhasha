# Model Adapter Guide

Bhasha now has adapter entry points for the assignment candidate models. These adapters are optional: they skip cleanly if dependencies, model files, reference clips, or external commands are missing.

## Adapter IDs

| Model | Adapter ID | Type | Notes |
| --- | --- | --- | --- |
| XTTS-v2 | `xtts_v2` | Python API | Uses Coqui `TTS.api.TTS`; requires reference audio. |
| Chatterbox | `chatterbox` | Python API | Uses `chatterbox.tts.ChatterboxTTS`; English only in current suite. |
| Fish Speech | `fish_speech_cli` | External command | Configure `command_template` after installing upstream repo. |
| CosyVoice2 | `cosyvoice_cli` | External command | Configure `command_template` after installing upstream repo. |
| Indic Parler-TTS | `indic_parler_tts` | Python API | Uses `parler_tts` and Transformers. |
| MMS-TTS | `hf_vits` | Python API | Uses Transformers `VitsModel` and `AutoTokenizer`. |
| Piper | `piper_cli` | CLI | Lightweight local baseline already verified. |

## Why External Command Adapters Exist

Fish Speech and CosyVoice2 change setup and inference scripts more often than simple PyPI packages. Bhasha therefore supports them through a configurable command template instead of hard-coding a brittle repo-specific command.

Example shape:

```json
"parameters": {
  "command_template": [
    "python",
    "path/to/infer.py",
    "--text", "{text}",
    "--language", "{language}",
    "--reference", "{reference_audio}",
    "--output", "{output_audio}"
  ]
}
```

The placeholders are:

- `{text}`
- `{language}`
- `{reference_audio}`
- `{output_audio}`
- `{model_id}`
- `{prompt_id}`

## Kaggle Strategy

Install and test one adapter at a time:

```bash
pip install -r requirements/xtts.txt
python -m bhasha run --suite configs/suites/multilingual_tts_takehome_v1.json --model xtts_v2 --language en --include-disabled
```

Then repeat for the next model. Do not compare speed metrics across different hardware sessions unless the GPU profile is the same and recorded.

## Reference Clips

Voice cloning adapters need valid reference clips under:

```text
data/references/en/reference.wav
data/references/ar/reference.wav
data/references/hi/reference.wav
```

Without those files, cloning adapters report skipped/missing reference behavior instead of fabricating speaker similarity.
