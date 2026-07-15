from __future__ import annotations

from bhasha.schema import GenerationRequest, GenerationResult

from ._shared import dependency_error, timed_generation, write_mono_wav_from_float
from .base import TTSAdapter


class HuggingFaceVitsAdapter(TTSAdapter):
    adapter_id = "hf_vits"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        try:
            import torch
            from transformers import AutoTokenizer, VitsModel
        except ModuleNotFoundError:
            return dependency_error("Transformers VITS dependencies are not installed. Install with `pip install -r requirements/hf_tts.txt`.")

        model_name = str(request.model.parameters.get("model_name", "facebook/mms-tts-eng"))
        model_by_language = request.model.parameters.get("model_by_language", {})
        if isinstance(model_by_language, dict):
            model_name = str(model_by_language.get(request.language.id, model_name))
        device = str(request.model.parameters.get("device", "cuda"))

        def _generate() -> None:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = VitsModel.from_pretrained(model_name).to(device)
            inputs = tokenizer(request.prompt.text, return_tensors="pt")
            inputs = {key: value.to(device) for key, value in inputs.items()}
            with torch.no_grad():
                output = model(**inputs).waveform
            sample_rate = int(model.config.sampling_rate)
            write_mono_wav_from_float(request.output_audio, output.detach().cpu().numpy(), sample_rate)

        return timed_generation(request, _generate)
