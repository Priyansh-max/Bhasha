from __future__ import annotations

from .base import TTSAdapter
from .chatterbox import ChatterboxAdapter
from .dummy import DummyToneAdapter
from .external_command import CosyVoiceCommandAdapter, FishSpeechCommandAdapter
from .hf_vits import HuggingFaceVitsAdapter
from .indic_parler import IndicParlerAdapter
from .piper_cli import PiperCliAdapter
from .xtts_v2 import XttsV2Adapter


_ADAPTERS: dict[str, type[TTSAdapter]] = {
    DummyToneAdapter.adapter_id: DummyToneAdapter,
    PiperCliAdapter.adapter_id: PiperCliAdapter,
    XttsV2Adapter.adapter_id: XttsV2Adapter,
    ChatterboxAdapter.adapter_id: ChatterboxAdapter,
    FishSpeechCommandAdapter.adapter_id: FishSpeechCommandAdapter,
    CosyVoiceCommandAdapter.adapter_id: CosyVoiceCommandAdapter,
    HuggingFaceVitsAdapter.adapter_id: HuggingFaceVitsAdapter,
    IndicParlerAdapter.adapter_id: IndicParlerAdapter,
}


def get_adapter(adapter_id: str) -> TTSAdapter:
    adapter_cls = _ADAPTERS.get(adapter_id)
    if adapter_cls is None:
        raise KeyError(f"No adapter registered for '{adapter_id}'")
    return adapter_cls()
