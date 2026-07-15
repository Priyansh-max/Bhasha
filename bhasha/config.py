from __future__ import annotations

import json
from pathlib import Path

from .schema import LanguageConfig, ModelConfig, PromptConfig, SuiteConfig


def load_suite(path: str | Path) -> SuiteConfig:
    suite_path = Path(path)
    raw = _load_config_file(suite_path)

    return SuiteConfig(
        suite_id=_required_str(raw, "suite_id"),
        name=_required_str(raw, "name"),
        description=_required_str(raw, "description"),
        output_root=Path(_required_str(raw, "output_root")),
        repeat_count=int(raw.get("repeat_count", 1)),
        languages=[_language(item) for item in raw.get("languages", [])],
        models=[_model(item) for item in raw.get("models", [])],
        prompts=[_prompt(item) for item in raw.get("prompts", [])],
    )


def _load_config_file(path: Path) -> dict:
    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8-sig") as handle:
            return json.load(handle)

    if path.suffix.lower() == ".toml":
        try:
            import tomllib as toml_reader
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "TOML suite files require Python 3.11+. Use the JSON suite file on Python 3.10."
            ) from exc

        with path.open("rb") as handle:
            return toml_reader.load(handle)

    raise ValueError(f"Unsupported suite config format: {path.suffix}")


def _required_str(data: dict, key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing required string field: {key}")
    return value


def _language(data: dict) -> LanguageConfig:
    return LanguageConfig(
        id=_required_str(data, "id"),
        name=_required_str(data, "name"),
        script=_required_str(data, "script"),
        asr_language=_required_str(data, "asr_language"),
    )


def _model(data: dict) -> ModelConfig:
    languages = data.get("languages", [])
    if not isinstance(languages, list) or not all(isinstance(item, str) for item in languages):
        raise ValueError(f"Model {data.get('id', '<unknown>')} has invalid languages")

    parameters = data.get("parameters", {})
    if not isinstance(parameters, dict):
        raise ValueError(f"Model {data.get('id', '<unknown>')} has invalid parameters")

    return ModelConfig(
        id=_required_str(data, "id"),
        name=_required_str(data, "name"),
        adapter=_required_str(data, "adapter"),
        enabled=bool(data.get("enabled", False)),
        supports_voice_cloning=bool(data.get("supports_voice_cloning", False)),
        license=_required_str(data, "license"),
        source=_required_str(data, "source"),
        languages=languages,
        parameters=parameters,
    )


def _prompt(data: dict) -> PromptConfig:
    reference_audio = data.get("reference_audio")
    if reference_audio is not None and not isinstance(reference_audio, str):
        raise ValueError(f"Prompt {data.get('id', '<unknown>')} has invalid reference_audio")

    return PromptConfig(
        id=_required_str(data, "id"),
        language=_required_str(data, "language"),
        category=_required_str(data, "category"),
        text=_required_str(data, "text"),
        reference_audio=reference_audio,
    )
