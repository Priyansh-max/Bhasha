# Model Candidate Matrix

This is the assignment candidate set. Local status is conservative: only lightweight Piper was run locally. Heavy models are configured/deferred until a fixed GPU environment is available.

| Language | Candidate | Task Fit | Local Status | Reason |
| --- | --- | --- | --- | --- |
| English | Piper en_US lessac medium | Fast baseline, no cloning | Ran locally | CPU-friendly baseline, real audio saved |
| English | Chatterbox / Turbo | Strong English cloning/naturalness | Deferred | Heavy dependency/model stack, not safe to run on laptop |
| English | Fish Speech | Cloning/multilingual candidate | Deferred | Heavy dependency/model stack |
| English | CosyVoice2 | Low-latency/streaming candidate | Deferred | Heavy dependency/model stack |
| Arabic | XTTS-v2 | Multilingual cloning candidate | Deferred | Needs heavier model install/GPU for fair run |
| Arabic | Fish Speech | Multilingual cloning candidate | Deferred | Heavy dependency/model stack |
| Arabic | MMS-TTS / Arabic fine-tune | Lightweight language-specific candidate | Deferred | Needs model selection/license verification |
| Hindi | Indic Parler-TTS | Hindi/Indic naturalness candidate | Deferred | Needs model install and likely GPU/large RAM |
| Hindi | XTTS-v2 | Multilingual cloning candidate | Deferred | Needs heavier model install/GPU for fair run |
| Hindi | MMS-TTS / Indic-TTS | Lightweight Indic baseline candidate | Deferred | Needs model selection/license verification |

No winner is claimed for Arabic or Hindi without measured audio. Bhasha records this honestly rather than fabricating metrics.
