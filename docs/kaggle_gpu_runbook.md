# Kaggle GPU Runbook

Use this when you are ready to test major models without stressing the laptop.

## 1. Create Notebook

- Create a Kaggle notebook.
- Enable GPU accelerator.
- Enable Internet.

## 2. Clone Bhasha

```bash
!git clone https://github.com/Priyansh-max/Bhasha.git
%cd Bhasha
!python --version
!nvidia-smi
```

## 3. Start With One Adapter

Do not install every model stack together. Start with one.

### XTTS-v2

```bash
!pip install -r requirements/xtts.txt
```

Add reference clips to:

```text
data/references/en/reference.wav
data/references/ar/reference.wav
data/references/hi/reference.wav
```

Then run one language first:

```bash
!python -m bhasha run \
  --suite configs/suites/multilingual_tts_core_v1.json \
  --model xtts_v2 \
  --language en \
  --include-disabled
```

### MMS-TTS

```bash
!pip install -r requirements/hf_tts.txt
!python -m bhasha run \
  --suite configs/suites/multilingual_tts_core_v1.json \
  --model mms_tts \
  --language hi \
  --include-disabled
```

### Indic Parler-TTS

```bash
!pip install -r requirements/indic_parler.txt
!python -m bhasha run \
  --suite configs/suites/multilingual_tts_core_v1.json \
  --model indic_parler_tts \
  --language hi \
  --include-disabled
```

### Chatterbox

```bash
!pip install -r requirements/chatterbox.txt
!python -m bhasha run \
  --suite configs/suites/multilingual_tts_core_v1.json \
  --model chatterbox \
  --language en \
  --include-disabled
```

## 4. Evaluate A Successful Run

Replace `<RUN_ID>` with the latest folder under `outputs/runs`.

```bash
!python -m bhasha eval-asr --run-dir outputs/runs/<RUN_ID> --model-size small --device cuda --compute-type float16
!python -m bhasha eval-speaker --run-dir outputs/runs/<RUN_ID> --device cuda
!python -m bhasha generate-report --run-dir outputs/runs/<RUN_ID>
```

Use `tiny` ASR for smoke tests and a stronger ASR model for final numbers if Kaggle resources allow.

## 5. Download Artifacts

```bash
!zip -r bhasha_outputs.zip outputs docs samples configs requirements
```

Download `bhasha_outputs.zip` from the Kaggle file browser.

## Rules

- Run one heavy model at a time.
- Record `nvidia-smi` output.
- Do not compare speed numbers across different GPU types.
- Do not report MOS until real listeners fill the rating CSV.
- Do not claim a language winner without real generated audio and metrics.

