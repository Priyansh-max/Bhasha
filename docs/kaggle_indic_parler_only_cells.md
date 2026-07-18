# Kaggle Indic Parler Only Cells

Use this in a fresh Kaggle notebook only.

Do not install XTTS, Chatterbox, or MMS in this notebook. This notebook is only for rescuing a second successful model: Indic Parler-TTS for Hindi.

Kaggle settings:

- Accelerator: GPU
- Internet: On

## Cell 1 - Environment Check

What it does:

- Confirms Python and GPU.

```python
!python --version
!nvidia-smi
```

## Cell 2 - Clone Updated Repo

What it does:

- Clones the repo fresh.
- Enters the project folder.
- Confirms the Indic adapter is present.

```python
%cd /kaggle/working

!rm -rf Bhasha
!git clone https://github.com/Priyansh-max/Bhasha.git

%cd /kaggle/working/Bhasha

!python -m py_compile bhasha/adapters/indic_parler.py
!cat requirements/indic_parler.txt
```

Important: only use this after pushing the updated Indic adapter and `requirements/indic_parler.txt` to GitHub. If you have not pushed, upload the repo zip instead of cloning.

## Cell 3 - Install Indic Parler Only

What it does:

- Installs only the Indic Parler dependency stack.
- Avoids XTTS/Chatterbox/MMS contamination.

```python
%cd /kaggle/working/Bhasha

!python -m pip install -q --upgrade pip setuptools wheel packaging
!python -m pip install -q --no-cache-dir -r requirements/indic_parler.txt
```

## Cell 4 - Preflight Import Check

What it does:

- Verifies the exact imports required by Indic Parler.
- If this fails, stop and paste the error.

```python
%cd /kaggle/working/Bhasha

import sys
import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

print("Python:", sys.executable)
print("torch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("Indic Parler imports OK")
```

## Cell 5 - Official Smoke Test

What it does:

- Runs the official Indic Parler usage pattern outside Bhasha.
- Produces one manual Hindi WAV.
- If this fails, do not run the benchmark yet.

```python
%cd /kaggle/working/Bhasha

from pathlib import Path
import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

Path("outputs/manual_smoke").mkdir(parents=True, exist_ok=True)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model_name = "ai4bharat/indic-parler-tts"

print("Loading", model_name, "on", device)
model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
prompt_tokenizer = AutoTokenizer.from_pretrained(model_name)
description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

prompt = "अरे, तुम आज कैसे हो?"
description = "Rohit's voice is clear and natural, with a moderate speed and pitch. The recording is very high quality, with the speaker's voice sounding clear and close up."

description_inputs = description_tokenizer(description, return_tensors="pt").to(device)
prompt_inputs = prompt_tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    generation = model.generate(
        input_ids=description_inputs.input_ids,
        attention_mask=description_inputs.attention_mask,
        prompt_input_ids=prompt_inputs.input_ids,
        prompt_attention_mask=prompt_inputs.attention_mask,
    )

audio = generation.detach().cpu().numpy().squeeze()
out = "outputs/manual_smoke/indic_parler_hindi_smoke.wav"
sf.write(out, audio, model.config.sampling_rate)
print("Wrote", out)
```

## Cell 6 - Run Bhasha Indic Parler Hindi

What it does:

- Runs the benchmark Hindi prompts through Indic Parler.
- Saves the run ID to `outputs/selected_run_ids.json`.

```python
%cd /kaggle/working/Bhasha

import subprocess
import json
from pathlib import Path

root = Path("outputs/runs")
root.mkdir(parents=True, exist_ok=True)
before = {p.name for p in root.iterdir() if p.is_dir()}

print("Running Indic Parler Hindi benchmark...")

result = subprocess.run(
    "python -m bhasha run --suite configs/suites/multilingual_tts_core_v1.json --model indic_parler_tts --language hi --include-disabled",
    shell=True,
    check=False,
)

new_dirs = [p for p in root.iterdir() if p.is_dir() and p.name not in before]
if new_dirs:
    run_dir = max(new_dirs, key=lambda p: p.stat().st_mtime)
else:
    run_dir = max([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime)

selected_path = Path("outputs/selected_run_ids.json")
selected = json.loads(selected_path.read_text()) if selected_path.exists() else {}
selected["indic_parler_hi"] = run_dir.name
selected_path.write_text(json.dumps(selected, indent=2))

print("Return code:", result.returncode)
print("INDIC_PARLER_HI_RUN_ID =", run_dir.name)
```

## Cell 7 - Inspect Benchmark Status

What it does:

- Shows whether Indic Parler produced real WAV files.
- Do not evaluate unless status is `success`.

```python
%cd /kaggle/working/Bhasha

import json
import pandas as pd
from pathlib import Path

selected = json.loads(Path("outputs/selected_run_ids.json").read_text())
run_id = selected["indic_parler_hi"]

print("INDIC_PARLER_HI_RUN_ID =", run_id)

df = pd.read_csv(f"outputs/runs/{run_id}/benchmark.csv")
display(df[[c for c in [
    "model_id",
    "language",
    "sample_id",
    "status",
    "audio_path",
    "audio_duration_seconds",
    "generation_time_seconds",
    "rtf",
    "failure_reason"
] if c in df.columns]])

print("Audio files:")
!find outputs/runs/$run_id -type f -name "*.wav"
```

## Cell 8 - Evaluate Indic Parler Hindi

Only run this if Cell 7 shows `success`.

What it does:

- Runs ASR WER/CER.
- Generates `results.md`.
- Speaker similarity is skipped because Indic Parler is not a cloning model.

```python
%cd /kaggle/working/Bhasha

import json
import subprocess
from pathlib import Path

selected = json.loads(Path("outputs/selected_run_ids.json").read_text())
run_id = selected["indic_parler_hi"]
run_dir = f"outputs/runs/{run_id}"

print("Evaluating Indic Parler:", run_id)

result = subprocess.run(
    f"python -m bhasha eval-asr --run-dir {run_dir} --model-size small --device cuda --compute-type float16",
    shell=True,
    check=False,
)

if result.returncode != 0:
    print("Small ASR failed; retrying tiny ASR")
    subprocess.run(
        f"python -m bhasha eval-asr --run-dir {run_dir} --model-size tiny --device cuda --compute-type float16",
        shell=True,
        check=False,
    )

subprocess.run(f"python -m bhasha generate-report --run-dir {run_dir}", shell=True, check=False)
```

## Cell 9 - Package Indic Outputs

What it does:

- Creates a zip containing the Indic Parler run, manual smoke audio, benchmark files, and reports.

```python
%cd /kaggle/working/Bhasha

!zip -r /kaggle/working/indic_parler_outputs.zip outputs configs requirements README.md docs
```

Download:

```text
/kaggle/working/indic_parler_outputs.zip
```

## If Indic Parler Fails

If Cell 5 fails, the model stack itself is not working in Kaggle.

If Cell 5 succeeds but Cell 6/7 fails, the issue is Bhasha integration. Paste the failure reason from Cell 7.

In the final submission, Indic Parler is a Hindi specialist comparison. Speaker similarity is `N/A` because it is not a cloning model.
