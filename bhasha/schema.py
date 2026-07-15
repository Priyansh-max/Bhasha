from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LanguageConfig:
    id: str
    name: str
    script: str
    asr_language: str


@dataclass(frozen=True)
class ModelConfig:
    id: str
    name: str
    adapter: str
    enabled: bool
    supports_voice_cloning: bool
    license: str
    source: str
    languages: list[str]
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PromptConfig:
    id: str
    language: str
    category: str
    text: str
    reference_audio: str | None = None


@dataclass(frozen=True)
class SuiteConfig:
    suite_id: str
    name: str
    description: str
    output_root: Path
    repeat_count: int
    languages: list[LanguageConfig]
    models: list[ModelConfig]
    prompts: list[PromptConfig]


@dataclass
class GenerationRequest:
    run_id: str
    sample_id: str
    language: LanguageConfig
    model: ModelConfig
    prompt: PromptConfig
    output_audio: Path
    reference_audio: Path | None = None


@dataclass
class GenerationResult:
    status: str
    output_audio: Path | None
    generation_time_seconds: float | None
    audio_duration_seconds: float | None
    latency_type: str
    time_to_first_audio_seconds: float | None = None
    failure_type: str | None = None
    failure_reason: str | None = None

    @property
    def rtf(self) -> float | None:
        if not self.generation_time_seconds or not self.audio_duration_seconds:
            return None
        if self.audio_duration_seconds <= 0:
            return None
        return self.generation_time_seconds / self.audio_duration_seconds
