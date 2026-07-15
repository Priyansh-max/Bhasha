from __future__ import annotations

import time

from bhasha.audio import wav_duration_seconds, write_tone_wav
from bhasha.schema import GenerationRequest, GenerationResult

from .base import TTSAdapter


class DummyToneAdapter(TTSAdapter):
    adapter_id = "dummy"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        start = time.perf_counter()
        # Make duration loosely depend on text length so benchmark plumbing sees varied audio lengths.
        duration = max(1.0, min(4.0, len(request.prompt.text.split()) * 0.28))
        write_tone_wav(request.output_audio, duration_seconds=duration)
        generation_time = time.perf_counter() - start
        audio_duration = wav_duration_seconds(request.output_audio)
        return GenerationResult(
            status="success",
            output_audio=request.output_audio,
            generation_time_seconds=generation_time,
            audio_duration_seconds=audio_duration,
            latency_type="batch_full_clip",
            time_to_first_audio_seconds=None,
        )
