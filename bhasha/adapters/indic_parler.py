from __future__ import annotations

from bhasha.schema import GenerationRequest, GenerationResult

from ._shared import dependency_error, timed_generation
from .base import TTSAdapter


class IndicParlerAdapter(TTSAdapter):
    adapter_id = "indic_parler_tts"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        try:
            import torch
            import soundfile as sf
            from parler_tts import ParlerTTSForConditionalGeneration
            from transformers import AutoTokenizer
        except ModuleNotFoundError:
            return dependency_error(
                "Indic Parler-TTS dependencies are not installed. "
                "Install with `pip install -r requirements/indic_parler.txt`."
            )

        model_name = str(request.model.parameters.get("model_name", "ai4bharat/indic-parler-tts"))
        device = str(request.model.parameters.get("device", "cuda"))
        description_by_language = request.model.parameters.get("description_by_language", {})
        if isinstance(description_by_language, dict) and request.language.id in description_by_language:
            description = str(description_by_language[request.language.id])
        else:
            description = str(
                request.model.parameters.get(
                    "description",
                    "Rohit's voice is clear and natural, with a moderate speed and pitch. "
                    "The recording is very high quality, with the speaker's voice sounding clear and close up.",
                )
            )

        def _generate() -> None:
            model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
            prompt_tokenizer = AutoTokenizer.from_pretrained(model_name)
            description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

            description_inputs = description_tokenizer(description, return_tensors="pt").to(device)
            prompt_inputs = prompt_tokenizer(request.prompt.text, return_tensors="pt").to(device)

            with torch.no_grad():
                generation = model.generate(
                    input_ids=description_inputs.input_ids,
                    attention_mask=description_inputs.attention_mask,
                    prompt_input_ids=prompt_inputs.input_ids,
                    prompt_attention_mask=prompt_inputs.attention_mask,
                )

            audio = generation.detach().cpu().numpy().squeeze()
            sample_rate = int(getattr(model.config, "sampling_rate", request.model.parameters.get("sample_rate", 44100)))
            sf.write(str(request.output_audio), audio, sample_rate)

        return timed_generation(request, _generate)

