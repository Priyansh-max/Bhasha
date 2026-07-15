from __future__ import annotations

from bhasha.schema import GenerationRequest, GenerationResult

from ._shared import dependency_error, timed_generation
from .base import TTSAdapter


class IndicParlerAdapter(TTSAdapter):
    adapter_id = "indic_parler_tts"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        try:
            import torch
            import torchaudio
            from parler_tts import ParlerTTSForConditionalGeneration
            from transformers import AutoTokenizer
        except ModuleNotFoundError:
            return dependency_error("Indic Parler-TTS dependencies are not installed. Install with `pip install -r requirements/indic_parler.txt`.")

        model_name = str(request.model.parameters.get("model_name", "ai4bharat/indic-parler-tts"))
        device = str(request.model.parameters.get("device", "cuda"))
        description = str(
            request.model.parameters.get(
                "description",
                "A clear, natural, studio-quality speaker voice with neutral emotion.",
            )
        )

        def _generate() -> None:
            model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            description_inputs = tokenizer(description, return_tensors="pt").to(device)
            prompt_inputs = tokenizer(request.prompt.text, return_tensors="pt").to(device)
            with torch.no_grad():
                generation = model.generate(
                    input_ids=description_inputs.input_ids,
                    attention_mask=description_inputs.attention_mask,
                    prompt_input_ids=prompt_inputs.input_ids,
                    prompt_attention_mask=prompt_inputs.attention_mask,
                )
            audio = generation.cpu().float()
            sample_rate = int(getattr(model.config, "sampling_rate", request.model.parameters.get("sample_rate", 24000)))
            torchaudio.save(str(request.output_audio), audio, sample_rate)

        return timed_generation(request, _generate)
