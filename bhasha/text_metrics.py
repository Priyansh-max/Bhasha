from __future__ import annotations

import unicodedata
from collections.abc import Sequence


def normalize_text(text: str) -> str:
    """Normalize text for round-trip ASR comparison.

    This is intentionally conservative: it lowercases where applicable, removes
    punctuation/symbols, normalizes Unicode forms, and collapses whitespace.
    Language-specific normalizers can be added later for stricter Arabic/Hindi
    handling.
    """
    normalized = unicodedata.normalize("NFKC", text).casefold()
    kept: list[str] = []
    previous_was_space = False

    for char in normalized:
        category = unicodedata.category(char)
        if category.startswith("P") or category.startswith("S"):
            if not previous_was_space:
                kept.append(" ")
                previous_was_space = True
            continue

        if char.isspace():
            if not previous_was_space:
                kept.append(" ")
                previous_was_space = True
            continue

        kept.append(char)
        previous_was_space = False

    return "".join(kept).strip()


def word_error_rate(reference: str, hypothesis: str) -> float:
    reference_words = normalize_text(reference).split()
    hypothesis_words = normalize_text(hypothesis).split()
    if not reference_words:
        return 0.0 if not hypothesis_words else 1.0
    return _levenshtein(reference_words, hypothesis_words) / len(reference_words)


def character_error_rate(reference: str, hypothesis: str) -> float:
    reference_chars = list(normalize_text(reference).replace(" ", ""))
    hypothesis_chars = list(normalize_text(hypothesis).replace(" ", ""))
    if not reference_chars:
        return 0.0 if not hypothesis_chars else 1.0
    return _levenshtein(reference_chars, hypothesis_chars) / len(reference_chars)


def _levenshtein(reference: Sequence[str], hypothesis: Sequence[str]) -> int:
    if len(reference) < len(hypothesis):
        reference, hypothesis = hypothesis, reference

    previous = list(range(len(hypothesis) + 1))
    for i, ref_item in enumerate(reference, start=1):
        current = [i]
        for j, hyp_item in enumerate(hypothesis, start=1):
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            substitution = previous[j - 1] + (ref_item != hyp_item)
            current.append(min(insertion, deletion, substitution))
        previous = current
    return previous[-1]
