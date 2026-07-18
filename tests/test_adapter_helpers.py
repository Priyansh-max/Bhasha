from pathlib import Path

from bhasha.adapters._shared import hf_token
from bhasha.adapters.indic_parler import _description_for_request
from bhasha.schema import GenerationRequest, LanguageConfig, ModelConfig, PromptConfig


def _request(parameters=None, language_id="hi"):
    language = LanguageConfig(id=language_id, name=language_id, script="", asr_language=language_id)
    model = ModelConfig(
        id="indic_parler_tts",
        name="Indic Parler-TTS",
        adapter="indic_parler_tts",
        enabled=True,
        supports_voice_cloning=False,
        license="test",
        source="test",
        languages=[language_id],
        parameters=parameters or {},
    )
    prompt = PromptConfig(id="p1", language=language_id, category="test", text="hello")
    return GenerationRequest(
        run_id="run",
        sample_id="sample",
        language=language,
        model=model,
        prompt=prompt,
        output_audio=Path("out.wav"),
    )


def test_hf_token_prefers_model_parameter(monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "env-token")
    request = _request({"hf_token": "param-token"})
    assert hf_token(request) == "param-token"


def test_hf_token_reads_environment(monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "env-token")
    request = _request()
    assert hf_token(request) == "env-token"


def test_hf_token_accepts_huggingface_hub_token(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.setenv("HUGGINGFACE_HUB_TOKEN", "hub-token")
    request = _request()
    assert hf_token(request) == "hub-token"


def test_indic_description_uses_language_specific_value():
    request = _request(
        {
            "description": "default voice",
            "description_by_language": {"hi": "hindi voice", "en": "english voice"},
        },
        language_id="hi",
    )
    assert _description_for_request(request) == "hindi voice"


def test_indic_description_falls_back_to_default():
    request = _request({"description": "default voice"}, language_id="en")
    assert _description_for_request(request) == "default voice"


def test_hf_token_required_raises_clear_error(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    monkeypatch.delenv("HUGGINGFACE_HUB_TOKEN", raising=False)
    request = _request()
    try:
        hf_token(request, required=True)
    except RuntimeError as exc:
        assert "HF_TOKEN" in str(exc)
    else:
        raise AssertionError("expected missing token error")
