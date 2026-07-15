from __future__ import annotations

from abc import ABC, abstractmethod

from bhasha.schema import GenerationRequest, GenerationResult


class TTSAdapter(ABC):
    adapter_id: str

    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate one audio sample for a benchmark request."""
