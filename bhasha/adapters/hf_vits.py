from __future__ import annotations

from bhasha.schema import GenerationRequest, GenerationResult

from ._shared import dependency_error, timed_generation
from .base import TTSAdapter


class HuggingFaceVitsAdapter(TTSAdapter):
    adapter_id = "hf_vits"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        try:
            import torch
            import soundfile as sf
            from transformers import AutoModelForTextToWaveform, AutoTokenizer, set_seed
        except ModuleNotFoundError:
            return dependency_error(
                "Transformers MMS/VITS dependencies are not installed. "
                "Install with `pip install -r requirements/hf_tts.txt`."
            )

        model_name = str(request.model.parameters.get("model_name", "facebook/mms-tts-eng"))
        model_by_language = request.model.parameters.get("model_by_language", {})
        if isinstance(model_by_language, dict):
            model_name = str(model_by_language.get(request.language.id, model_name))
        device = str(request.model.parameters.get("device", "cuda"))
        seed = int(request.model.parameters.get("seed", 555))

        def _generate() -> None:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForTextToWaveform.from_pretrained(model_name).to(device)
            inputs = tokenizer(text=request.prompt.text, return_tensors="pt").to(device)
            set_seed(seed)
            with torch.no_grad():
                waveform = model(**inputs).waveform[0].detach().cpu().numpy()
            sf.write(str(request.output_audio), waveform, int(model.config.sampling_rate))

        return timed_generation(request, _generate)
