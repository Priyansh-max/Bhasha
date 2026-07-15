# Requirements

These files pin small, task-specific dependency sets instead of forcing every benchmark backend into one environment.

- `piper.txt`: CPU-friendly Piper baseline used for the first real TTS smoke run.

Heavy model stacks such as XTTS, Fish Speech, CosyVoice, Whisper, and speaker-embedding models should get separate requirement files or environment notes so dependency conflicts stay visible.
