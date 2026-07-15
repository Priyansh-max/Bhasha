from __future__ import annotations

from bhasha.schema import GenerationRequest, GenerationResult

from ._shared import dependency_error, language_code, require_reference_audio, timed_generation
from .base import TTSAdapter


class XttsV2Adapter(TTSAdapter):
    adapter_id = "xtts_v2"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        try:
            from TTS.api import TTS
        except ModuleNotFoundError:
            return dependency_error("Coqui TTS is not installed. Install with `pip install -r requirements/xtts.txt`.")

        speaker_wav = require_reference_audio(request)
        if speaker_wav is None:
            return dependency_error("XTTS-v2 requires a valid reference audio clip for voice cloning.")

        model_name = str(request.model.parameters.get("model_name", "tts_models/multilingual/multi-dataset/xtts_v2"))
        device = str(request.model.parameters.get("device", "cuda"))

        def _generate() -> None:
            tts = TTS(model_name=model_name)
            if hasattr(tts, "to"):
                tts = tts.to(device)
            tts.tts_to_file(
                text=request.prompt.text,
                speaker_wav=str(speaker_wav),
                language=language_code(request),
                file_path=str(request.output_audio),
            )

        return timed_generation(request, _generate)
