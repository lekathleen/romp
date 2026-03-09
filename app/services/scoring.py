def apply_threshold(average_score: float | None, threshold: float) -> dict:
    if average_score is None:
        return {"average_score": None, "is_planned": False}
    return {"average_score": average_score, "is_planned": average_score <= threshold}
