from __future__ import annotations

from pathlib import Path

from .base import ASRBackendError, ASRTranscript


class FasterWhisperASR:
    def __init__(self, *, model_size: str, device: str, compute_type: str) -> None:
        try:
            from faster_whisper import WhisperModel
        except ModuleNotFoundError as exc:
            raise ASRBackendError(
                "faster-whisper is not installed. Install it with `pip install -r requirements/asr.txt`."
            ) from exc

        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    @property
    def model_label(self) -> str:
        return f"faster-whisper:{self.model_size}:{self.device}:{self.compute_type}"

    def transcribe(self, audio_path: str | Path, *, language: str | None) -> ASRTranscript:
        segments, info = self.model.transcribe(str(audio_path), language=language)
        text = " ".join(segment.text.strip() for segment in segments).strip()
        return ASRTranscript(
            text=text,
            language=getattr(info, "language", None),
            duration_seconds=getattr(info, "duration", None),
        )
