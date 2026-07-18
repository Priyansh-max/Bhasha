from __future__ import annotations

import time
from pathlib import Path
from typing import Callable

from bhasha.audio import wav_duration_seconds
from bhasha.schema import GenerationRequest, GenerationResult


def dependency_error(message: str) -> GenerationResult:
    return GenerationResult(
        status="skipped",
        output_audio=None,
        generation_time_seconds=None,
        audio_duration_seconds=None,
        latency_type="batch_full_clip",
        failure_type="dependency_error",
        failure_reason=message,
    )


def skipped_model_file(message: str) -> GenerationResult:
    return GenerationResult(
        status="skipped",
        output_audio=None,
        generation_time_seconds=None,
        audio_duration_seconds=None,
        latency_type="batch_full_clip",
        failure_type="dependency_error",
        failure_reason=message,
    )


def model_error(message: str, *, generation_time_seconds: float | None = None) -> GenerationResult:
    return GenerationResult(
        status="failed",
        output_audio=None,
        generation_time_seconds=generation_time_seconds,
        audio_duration_seconds=None,
        latency_type="batch_full_clip",
        failure_type="model_error",
        failure_reason=message,
    )


def timed_generation(request: GenerationRequest, generate_fn: Callable[[], None]) -> GenerationResult:
    request.output_audio.parent.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    try:
        generate_fn()
    except Exception as exc:
        return model_error(str(exc), generation_time_seconds=time.perf_counter() - start)

    generation_time = time.perf_counter() - start
    if not request.output_audio.exists():
        return model_error(
            "Generation finished but did not create the expected audio file.",
            generation_time_seconds=generation_time,
        )

    return GenerationResult(
        status="success",
        output_audio=request.output_audio,
        generation_time_seconds=generation_time,
        audio_duration_seconds=wav_duration_seconds(request.output_audio),
        latency_type="batch_full_clip",
    )


def hf_token(request: GenerationRequest, *, required: bool = False) -> str | None:
    import os

    raw = request.model.parameters.get("hf_token") or request.model.parameters.get("token")
    token = str(raw).strip() if raw else os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
    token = token.strip() if token else None
    if required and not token:
        raise RuntimeError(
            "This Hugging Face model requires access. Set HF_TOKEN or HUGGINGFACE_HUB_TOKEN, "
            "or add hf_token to the model parameters."
        )
    return token

def language_code(request: GenerationRequest) -> str:
    mapping = request.model.parameters.get("language_map", {})
    if isinstance(mapping, dict) and request.language.id in mapping:
        return str(mapping[request.language.id])
    return request.language.id


def reference_audio_path(request: GenerationRequest) -> Path | None:
    if request.reference_audio:
        return request.reference_audio
    raw = request.model.parameters.get("speaker_wav") or request.model.parameters.get("reference_audio")
    return Path(str(raw)) if raw else None


def require_reference_audio(request: GenerationRequest) -> Path | None:
    path = reference_audio_path(request)
    if path is None or not path.exists():
        return None
    return path


def float_waveform_to_int16(waveform) -> bytes:
    import numpy as np

    array = np.asarray(waveform, dtype=np.float32).reshape(-1)
    array = np.clip(array, -1.0, 1.0)
    int16 = (array * 32767.0).astype("<i2")
    return int16.tobytes()


def write_mono_wav_from_float(path: str | Path, waveform, sample_rate: int) -> None:
    import wave

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(float_waveform_to_int16(waveform))


