# Candidate Matrix

This matrix records adapter availability and local example status. Heavy models have optional adapters, but actual inference should be run on a suitable fixed GPU profile.

| Language | Candidate | Task Fit | Local Example Status | Reason |
| --- | --- | --- | --- | --- |
| English | Piper en_US lessac medium | Fast baseline, no cloning | Ran locally | CPU-friendly baseline, real audio saved |
| English | Chatterbox / Turbo | Strong English cloning/naturalness | Adapter added, dependency deferred | Heavy dependency/model stack |
| English | Fish Speech | Cloning/multilingual candidate | External-command adapter added | Requires upstream repo command configuration |
| English | CosyVoice2 | Low-latency/streaming candidate | External-command adapter added | Requires upstream repo command configuration |
| Arabic | XTTS-v2 | Multilingual cloning candidate | Adapter added, dependency deferred | Needs reference clip and heavier model install |
| Arabic | Fish Speech | Multilingual cloning candidate | External-command adapter added | Requires upstream repo command configuration |
| Arabic | MMS-TTS / Arabic fine-tune | Lightweight language-specific candidate | Adapter added, dependency deferred | Uses Transformers VITS/MMS path |
| Hindi | Indic Parler-TTS | Hindi/Indic naturalness candidate | Adapter added, dependency deferred | Needs model install and likely GPU/large RAM |
| Hindi | XTTS-v2 | Multilingual cloning candidate | Adapter added, dependency deferred | Needs reference clip and heavier model install |
| Hindi | MMS-TTS / Indic-TTS | Lightweight Indic baseline candidate | Adapter added, dependency deferred | Uses Transformers VITS/MMS path |

No winner is claimed for candidates that were not actually run.
