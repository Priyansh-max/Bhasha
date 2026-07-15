from __future__ import annotations

import shlex
import shutil
import subprocess

from bhasha.schema import GenerationRequest, GenerationResult

from ._shared import dependency_error, language_code, model_error, reference_audio_path, timed_generation
from .base import TTSAdapter


class ExternalCommandAdapter(TTSAdapter):
    adapter_id = "external_command"
    model_label = "external command"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        template = request.model.parameters.get("command_template")
        if not template:
            return dependency_error(
                f"No command_template configured for {request.model.id}. Install the model repo and add its inference command."
            )

        command = _format_command(template, request)
        executable = command[0]
        if shutil.which(executable) is None:
            return dependency_error(f"Executable not found for {request.model.id}: {executable}")

        stdin_text = request.prompt.text if bool(request.model.parameters.get("stdin_text", False)) else None

        def _generate() -> None:
            completed = subprocess.run(
                command,
                input=stdin_text,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if completed.returncode != 0:
                raise RuntimeError((completed.stderr or completed.stdout or "Command failed").strip())

        return timed_generation(request, _generate)


class FishSpeechCommandAdapter(ExternalCommandAdapter):
    adapter_id = "fish_speech_cli"
    model_label = "Fish Speech CLI"


class CosyVoiceCommandAdapter(ExternalCommandAdapter):
    adapter_id = "cosyvoice_cli"
    model_label = "CosyVoice CLI"


def _format_command(template, request: GenerationRequest) -> list[str]:
    reference_audio = reference_audio_path(request)
    values = {
        "text": request.prompt.text,
        "language": language_code(request),
        "output_audio": str(request.output_audio),
        "reference_audio": str(reference_audio) if reference_audio else "",
        "model_id": request.model.id,
        "prompt_id": request.prompt.id,
    }
    if isinstance(template, str):
        parts = shlex.split(template)
    elif isinstance(template, list):
        parts = [str(item) for item in template]
    else:
        raise TypeError("command_template must be a string or list of strings")
    return [part.format(**values) for part in parts]
