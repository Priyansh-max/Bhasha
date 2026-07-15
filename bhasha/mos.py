from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, pstdev


@dataclass
class MOSRating:
    sample_id: str
    listener_id: str
    score: float
    same_speaker_ab: str = ""
    notes: str = ""


@dataclass
class MOSAggregation:
    sample_id: str
    mos: float | None
    rating_count: int
    score_std: float | None
    ratings: list[MOSRating] = field(default_factory=list)


def parse_mos_score(raw_score: str) -> float | None:
    value = raw_score.strip()
    if not value:
        return None
    try:
        score = float(value)
    except ValueError as exc:
        raise ValueError(f"MOS score must be numeric, got {raw_score!r}") from exc
    if score < 1.0 or score > 5.0:
        raise ValueError(f"MOS score must be between 1 and 5, got {score}")
    return score


def aggregate_mos_ratings(ratings: list[MOSRating]) -> dict[str, MOSAggregation]:
    grouped: dict[str, list[MOSRating]] = {}
    for rating in ratings:
        grouped.setdefault(rating.sample_id, []).append(rating)

    aggregations: dict[str, MOSAggregation] = {}
    for sample_id, sample_ratings in grouped.items():
        scores = [rating.score for rating in sample_ratings]
        aggregations[sample_id] = MOSAggregation(
            sample_id=sample_id,
            mos=mean(scores) if scores else None,
            rating_count=len(scores),
            score_std=pstdev(scores) if len(scores) > 1 else 0.0 if scores else None,
            ratings=sample_ratings,
        )
    return aggregations
