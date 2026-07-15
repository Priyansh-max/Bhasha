from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ASRTranscript:
    text: str
    language: str | None
    duration_seconds: float | None


class ASRBackendError(RuntimeError):
    pass
