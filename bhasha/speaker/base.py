from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SpeakerEmbedding:
    vector: list[float]
    sample_rate: int | None


class SpeakerBackendError(RuntimeError):
    pass


class SpeakerEmbeddingBackend:
    @property
    def model_label(self) -> str:
        raise NotImplementedError

    def embed(self, audio_path: str | Path) -> SpeakerEmbedding:
        raise NotImplementedError
