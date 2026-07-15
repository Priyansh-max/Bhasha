from __future__ import annotations

from .base import TTSAdapter
from .dummy import DummyToneAdapter


_ADAPTERS: dict[str, type[TTSAdapter]] = {
    DummyToneAdapter.adapter_id: DummyToneAdapter,
}


def get_adapter(adapter_id: str) -> TTSAdapter:
    adapter_cls = _ADAPTERS.get(adapter_id)
    if adapter_cls is None:
        raise KeyError(f"No adapter registered for '{adapter_id}'")
    return adapter_cls()
