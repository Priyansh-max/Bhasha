from __future__ import annotations

import math
import wave
from pathlib import Path


def wav_duration_seconds(path: str | Path) -> float:
    with wave.open(str(path), "rb") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
    return frames / float(rate)


def write_tone_wav(
    path: str | Path,
    *,
    duration_seconds: float,
    sample_rate: int = 16_000,
    frequency_hz: float = 440.0,
    amplitude: float = 0.2,
) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    total_frames = int(duration_seconds * sample_rate)
    max_int16 = 32767

    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        frames = bytearray()
        for index in range(total_frames):
            sample = amplitude * math.sin(2 * math.pi * frequency_hz * index / sample_rate)
            value = int(sample * max_int16)
            frames += value.to_bytes(2, byteorder="little", signed=True)
        wav.writeframes(frames)
