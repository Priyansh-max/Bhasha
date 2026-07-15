from __future__ import annotations

import math
from collections.abc import Sequence


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Cosine similarity requires vectors with the same length")
    if not left:
        raise ValueError("Cosine similarity requires non-empty vectors")

    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("Cosine similarity is undefined for zero vectors")
    return dot / (left_norm * right_norm)
