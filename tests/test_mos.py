from bhasha.mos import MOSRating, aggregate_mos_ratings, parse_mos_score


def test_parse_blank_mos_score_returns_none():
    assert parse_mos_score("") is None


def test_parse_valid_mos_score():
    assert parse_mos_score("4.5") == 4.5


def test_aggregate_mos_ratings():
    result = aggregate_mos_ratings([
        MOSRating(sample_id="a", listener_id="r1", score=4.0),
        MOSRating(sample_id="a", listener_id="r2", score=5.0),
    ])
    assert result["a"].mos == 4.5
    assert result["a"].rating_count == 2
