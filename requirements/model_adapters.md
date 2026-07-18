# Model Adapter Dependency Notes

Use fresh environments for heavy adapters.

## Indic Parler-TTS

```bash
export HF_TOKEN=hf_...
pip install -r requirements/indic_parler.txt
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model indic_parler_tts --language hi --include-disabled
```

The model `ai4bharat/indic-parler-tts` is gated. Accept access on Hugging Face before running.

## MMS-TTS

```bash
pip install -r requirements/hf_tts.txt
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model mms_tts --language ar --include-disabled
```

The adapter uses `AutoModelForTextToWaveform` and `uroman` for non-Roman scripts.

## XTTS-v2

```bash
pip install -r requirements/xtts.txt
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model xtts_v2 --language en --include-disabled
```

Requires reference audio under `data/references/<lang>/reference.wav`.

## Chatterbox

```bash
pip install -r requirements/chatterbox.txt
python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model chatterbox --language en --include-disabled
```

If package import errors occur on Python 3.12, try Python 3.11.
