from __future__ import annotations

from collections import Counter
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReviewOutcome = Literal["accept", "reject", "abstain", "needs_review"]


class ReviewRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    row_id: str = Field(min_length=5)
    reviewer_id: str = Field(min_length=1)
    outcome: ReviewOutcome
    severity: Literal["low", "medium", "high", "critical"]
    notes: str = Field(min_length=1)


class AdjudicationRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    row_id: str = Field(min_length=5)
    outcome: ReviewOutcome
    reviewer_ids: list[str] = Field(min_length=2)
    rationale: str = Field(min_length=1)


def adjudicate_reviews(reviews: list[ReviewRecord]) -> AdjudicationRecord:
    if len(reviews) < 2:
        raise ValueError("ambiguous or high-severity rows require two reviews")
    if len({review.reviewer_id for review in reviews}) < 2:
        raise ValueError("reviews must come from independent reviewers")
    if len({review.row_id for review in reviews}) != 1:
        raise ValueError("all reviews must refer to one row")
    counts = Counter(review.outcome for review in reviews)
    outcome, count = counts.most_common(1)[0]
    final = outcome if count > len(reviews) / 2 else "needs_review"
    return AdjudicationRecord(
        row_id=reviews[0].row_id,
        outcome=final,
        reviewer_ids=sorted({review.reviewer_id for review in reviews}),
        rationale="; ".join(review.notes for review in reviews),
    )
