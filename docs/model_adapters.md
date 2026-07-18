# Model Adapter Guide

Bhasha includes optional adapters for the TTS candidates used in the benchmark. Install and run one heavy model stack at a time, preferably in a fresh virtual environment, because open-source TTS projects often pin different Torch, Transformers, audio, and protobuf versions.

## Adapter IDs

| Model | CLI model id | Adapter | Cloning | Notes |
| --- | --- | --- | --- | --- |
| XTTS-v2 | `xtts_v2` | `xtts_v2` | Yes | Requires a reference WAV per language. |
| Chatterbox | `chatterbox` | `chatterbox` | Yes | English candidate; best on Python 3.11-style environments. |
| Indic Parler-TTS | `indic_parler_tts` | `indic_parler_tts` | No | English/Hindi in the core suite; gated HF model, set `HF_TOKEN`. |
| MMS-TTS | `mms_tts` | `hf_vits` | No | English/Arabic/Hindi baseline via Hugging Face TextToWaveform. |
| Fish Speech | `fish_speech` | `fish_speech_cli` | Yes | External repo command wrapper; configure `command_template`. |
| CosyVoice2 | `cosyvoice2` | `cosyvoice_cli` | Yes | External repo command wrapper; configure `command_template`. |
| Piper | `piper_cli` | `piper_cli` | No | Lightweight local CPU baseline. |

## Common CLI Pattern

Inspect the suite:

```bash
python -m bhasha inspect --suite configs/suites/multilingual_tts_core_v1.json
```

Run one model/language pair:

```bash
python -m bhasha run \
  --suite configs/suites/multilingual_tts_core_v1.json \
  --model xtts_v2 \
  --language en \
  --include-disabled
```

Evaluate a completed run:

```bash
python -m bhasha eval-asr --run-dir outputs/runs/<run_id> --model-size small --device cuda --compute-type float16
python -m bhasha eval-speaker --run-dir outputs/runs/<run_id> --device cuda
python -m bhasha generate-report --run-dir outputs/runs/<run_id>
```

Speaker similarity only applies to cloning models with a valid reference clip.

## Reference Clips For Cloning

XTTS-v2 and Chatterbox need reference audio. Put consented clips here:

```text
data/references/en/reference.wav
data/references/ar/reference.wav
data/references/hi/reference.wav
```

Indic Parler-TTS and MMS-TTS do not clone the reference speaker, so speaker similarity should be reported as `not_applicable` for those models.

## Hugging Face Tokens

Some Hugging Face models are gated. The adapters read tokens from either model parameters or environment variables:

```bash
export HF_TOKEN=hf_...
# or
export HUGGINGFACE_HUB_TOKEN=hf_...
```

On Windows PowerShell:

```powershell
$env:HF_TOKEN = "hf_..."
```

Indic Parler-TTS currently requires access to `ai4bharat/indic-parler-tts`. Accept/request access on Hugging Face, then set `HF_TOKEN` before running:

```bash
pip install -r requirements/indic_parler.txt
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model indic_parler_tts --language hi --include-disabled
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model indic_parler_tts --language en --include-disabled
```

## MMS-TTS

MMS-TTS uses `AutoModelForTextToWaveform`, `soundfile`, and `uroman` for non-Roman scripts.

```bash
pip install -r requirements/hf_tts.txt
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model mms_tts --language en --include-disabled
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model mms_tts --language ar --include-disabled
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model mms_tts --language hi --include-disabled
```

## External Repo Adapters

Fish Speech and CosyVoice2 are repository-style integrations. Install their upstream repos separately, then configure `command_template` in the suite. Bhasha will format these placeholders:

- `{text}`
- `{language}`
- `{reference_audio}`
- `{output_audio}`
- `{model_id}`
- `{prompt_id}`

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
