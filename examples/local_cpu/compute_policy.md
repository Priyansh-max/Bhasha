# Local CPU Compute Profile

This example uses a conservative local compute profile.

## Policy

The local machine is used for lightweight validation:

- Framework development
- Config validation
- Piper CPU baseline
- Tiny faster-whisper ASR evaluation
- CSV/Markdown report generation
- Failure/dependency recording for unavailable adapters

## Deferred Work

The following should be run on a fixed GPU profile rather than a constrained local machine:

- Fish Speech
- CosyVoice2
- Chatterbox full comparison
- XTTS-v2 multilingual cloning runs
- Whisper large-v3 final ASR scoring
- SpeechBrain speaker scoring on larger batches

Speed metrics from different hardware profiles must not be mixed.
