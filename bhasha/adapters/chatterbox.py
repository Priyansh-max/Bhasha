from __future__ import annotations

from bhasha.schema import GenerationRequest, GenerationResult

from ._shared import dependency_error, reference_audio_path, timed_generation
from .base import TTSAdapter


class ChatterboxAdapter(TTSAdapter):
    adapter_id = "chatterbox"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        try:
            import torchaudio
            from chatterbox.tts import ChatterboxTTS
        except ModuleNotFoundError:
            return dependency_error("Chatterbox is not installed. Install with `pip install -r requirements/chatterbox.txt`.")

        device = str(request.model.parameters.get("device", "cuda"))
        audio_prompt = reference_audio_path(request)

        def _generate() -> None:
            model = ChatterboxTTS.from_pretrained(device=device)
            kwargs = {}
            if audio_prompt is not None and audio_prompt.exists():
                kwargs["audio_prompt_path"] = str(audio_prompt)
            wav = model.generate(request.prompt.text, **kwargs)
            sample_rate = int(getattr(model, "sr", request.model.parameters.get("sample_rate", 24000)))
            torchaudio.save(str(request.output_audio), wav, sample_rate)

        return timed_generation(request, _generate)
