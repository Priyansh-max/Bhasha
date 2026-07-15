from __future__ import annotations

from pathlib import Path

from .base import SpeakerBackendError, SpeakerEmbedding, SpeakerEmbeddingBackend


class SpeechBrainSpeakerEmbedding(SpeakerEmbeddingBackend):
    def __init__(
        self,
        *,
        source: str = "speechbrain/spkrec-ecapa-voxceleb",
        savedir: str = "models/speaker/speechbrain-spkrec-ecapa-voxceleb",
        device: str = "cpu",
    ) -> None:
        try:
            import torch
            import torchaudio
            try:
                from speechbrain.inference.speaker import EncoderClassifier
            except ModuleNotFoundError:
                from speechbrain.pretrained import EncoderClassifier
        except ModuleNotFoundError as exc:
            raise SpeakerBackendError(
                "SpeechBrain speaker embedding dependencies are not installed. "
                "Install them with `pip install -r requirements/speaker.txt`."
            ) from exc

        self.torch = torch
        self.torchaudio = torchaudio
        self.source = source
        self.savedir = savedir
        self.device = device
        run_opts = {"device": device}
        try:
            self.classifier = EncoderClassifier.from_hparams(
                source=source,
                savedir=savedir,
                run_opts=run_opts,
            )
        except Exception as exc:
            raise SpeakerBackendError(f"Failed to load SpeechBrain speaker model {source!r}: {exc}") from exc

    @property
    def model_label(self) -> str:
        return f"speechbrain:{self.source}:{self.device}"

    def embed(self, audio_path: str | Path) -> SpeakerEmbedding:
        try:
            signal, sample_rate = self.torchaudio.load(str(audio_path))
            if signal.shape[0] > 1:
                signal = signal.mean(dim=0, keepdim=True)
            if sample_rate != 16000:
                signal = self.torchaudio.transforms.Resample(sample_rate, 16000)(signal)
                sample_rate = 16000
            signal = signal.to(self.device)
            with self.torch.no_grad():
                embedding = self.classifier.encode_batch(signal).squeeze().detach().cpu().tolist()
        except Exception as exc:
            raise SpeakerBackendError(f"Failed to embed audio {audio_path!s}: {exc}") from exc

        if isinstance(embedding, float):
            vector = [embedding]
        else:
            vector = [float(value) for value in embedding]
        return SpeakerEmbedding(vector=vector, sample_rate=sample_rate)
