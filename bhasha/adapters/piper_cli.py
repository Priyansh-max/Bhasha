from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path

from bhasha.audio import wav_duration_seconds
from bhasha.schema import GenerationRequest, GenerationResult

from .base import TTSAdapter


class PiperCliAdapter(TTSAdapter):
    adapter_id = "piper_cli"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        executable = str(request.model.parameters.get("executable", "piper"))
        resolved_executable = shutil.which(executable)
        if resolved_executable is None:
            return GenerationResult(
                status="skipped",
                output_audio=None,
                generation_time_seconds=None,
                audio_duration_seconds=None,
                latency_type="batch_full_clip",
                failure_type="dependency_error",
                failure_reason=f"Piper executable not found: {executable}. Install with `pip install piper-tts==1.4.2`.",
            )

        model_path = _required_model_file(request, "model_path")
        if model_path is None:
            return _missing_file_result(request, "model_path")

        config_path = _optional_model_file(request, "config_path")
        if config_path is None and request.model.parameters.get("config_path"):
            return _missing_file_result(request, "config_path")

        request.output_audio.parent.mkdir(parents=True, exist_ok=True)

        command = [
            resolved_executable,
            "--model",
            str(model_path),
            "--output_file",
            str(request.output_audio),
        ]
        if config_path is not None:
            command.extend(["--config", str(config_path)])

        speaker = request.model.parameters.get("speaker")
        if speaker is not None:
            command.extend(["--speaker", str(speaker)])

        length_scale = request.model.parameters.get("length_scale")
        if length_scale is not None:
            command.extend(["--length_scale", str(length_scale)])

        noise_scale = request.model.parameters.get("noise_scale")
        if noise_scale is not None:
            command.extend(["--noise_scale", str(noise_scale)])

        noise_w = request.model.parameters.get("noise_w")
        if noise_w is not None:
            command.extend(["--noise_w", str(noise_w)])

        start = time.perf_counter()
        try:
            completed = subprocess.run(
                command,
                input=request.prompt.text,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except Exception as exc:
            return GenerationResult(
                status="failed",
                output_audio=None,
                generation_time_seconds=time.perf_counter() - start,
                audio_duration_seconds=None,
                latency_type="batch_full_clip",
                failure_type="model_error",
                failure_reason=str(exc),
            )

        generation_time = time.perf_counter() - start
        if completed.returncode != 0:
            return GenerationResult(
                status="failed",
                output_audio=None,
                generation_time_seconds=generation_time,
                audio_duration_seconds=None,
                latency_type="batch_full_clip",
                failure_type="model_error",
                failure_reason=(completed.stderr or completed.stdout or "Piper exited with a non-zero status").strip(),
            )

        if not request.output_audio.exists():
            return GenerationResult(
                status="failed",
                output_audio=None,
                generation_time_seconds=generation_time,
                audio_duration_seconds=None,
                latency_type="batch_full_clip",
                failure_type="model_error",
                failure_reason="Piper completed but did not create the expected WAV file.",
            )

        return GenerationResult(
            status="success",
            output_audio=request.output_audio,
            generation_time_seconds=generation_time,
            audio_duration_seconds=wav_duration_seconds(request.output_audio),
            latency_type="batch_full_clip",
        )


def _required_model_file(request: GenerationRequest, key: str) -> Path | None:
    raw_path = request.model.parameters.get(key)
    if not raw_path:
        return None
    path = Path(str(raw_path))
    return path if path.exists() else None


def _optional_model_file(request: GenerationRequest, key: str) -> Path | None:
    raw_path = request.model.parameters.get(key)
    if not raw_path:
        return None
    path = Path(str(raw_path))
    return path if path.exists() else None


def _missing_file_result(request: GenerationRequest, key: str) -> GenerationResult:
    return GenerationResult(
        status="skipped",
        output_audio=None,
        generation_time_seconds=None,
        audio_duration_seconds=None,
        latency_type="batch_full_clip",
        failure_type="dependency_error",
        failure_reason=f"Missing Piper {key}: {request.model.parameters.get(key)!r}. Run `python scripts/download_piper_voice.py`.",
    )
