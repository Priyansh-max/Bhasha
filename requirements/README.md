# Requirements

Install one model stack at a time. Do not install every heavy TTS backend into one environment unless you are prepared to resolve Torch, Transformers, protobuf, and audio-library conflicts.

Recommended environments:

- `xtts.txt`: XTTS-v2 cloning baseline.
- `indic_parler.txt`: Indic Parler-TTS. Requires Hugging Face access and `HF_TOKEN` for `ai4bharat/indic-parler-tts`.
- `hf_tts.txt`: MMS-TTS via Hugging Face TextToWaveform.
- `chatterbox.txt`: Chatterbox English candidate; prefer Python 3.11 if possible.
- `asr.txt`: faster-whisper ASR for WER/CER.
- `speaker.txt`: SpeechBrain speaker embeddings for cloning similarity.
- `piper.txt`: lightweight local CPU baseline.

External repository models such as Fish Speech and CosyVoice2 should be installed in their own environments and wired through `command_template` in the suite.
