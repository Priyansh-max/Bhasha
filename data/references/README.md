# Reference Voice Clips

Voice cloning evaluation requires consented or openly licensed reference clips.

For final assignment runs, place reference audio here:

```text
data/references/en/reference.wav
data/references/ar/reference.wav
data/references/hi/reference.wav
```

Recommended clip properties:

- 10-30 seconds
- single speaker
- quiet background
- no music
- WAV preferred
- document source and license in `reference_clips.csv`

Do not clone a real person without consent. If no valid reference clip is available, Bhasha records speaker similarity as `missing_reference_audio` instead of inventing a score.
