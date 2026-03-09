import pytest

from app.services.scoring import apply_threshold


@pytest.mark.parametrize(
    "average_score, threshold, expected_planned",
    [
        (1.5, 2.0, True),
        (2.0, 2.0, True),
        (2.1, 2.0, False),
        (None, 2.0, False),
    ],
)
def test_apply_threshold(average_score, threshold, expected_planned):
    result = apply_threshold(average_score=average_score, threshold=threshold)
    assert result["is_planned"] == expected_planned


def test_apply_threshold_none():
    result = apply_threshold(average_score=None, threshold=2.0)
    assert result["average_score"] is None
    assert not result["is_planned"]
