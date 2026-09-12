import pytest
from pydantic import ValidationError

from nhscopilot_eval.adjudication import ReviewRecord, adjudicate_reviews
from nhscopilot_eval.contracts import PublicDevelopmentRow
from nhscopilot_eval.provenance import make_content_hash, make_row_id


def test_duplicate_reviewer_cannot_manufacture_majority() -> None:
    reviews = [
        ReviewRecord(
            row_id="row-synthetic-review",
            reviewer_id=reviewer_id,
            outcome=outcome,
            severity="high",
            notes="synthetic fixture review",
        )
        for reviewer_id, outcome in (
            ("reviewer-a", "accept"),
            ("reviewer-a", "accept"),
            ("reviewer-b", "reject"),
        )
    ]

    with pytest.raises(ValueError, match="duplicate reviewer"):
        adjudicate_reviews(reviews)


def _public_row_data() -> dict[str, str]:
    prompt = "Synthetic public contract fixture."
    source_id = "synthetic-authored-project09"
    split = "public_development"
    return {
        "row_id": make_row_id("guidance", prompt, source_id, split),
        "category": "guidance",
        "prompt": prompt,
        "source_id": source_id,
        "source_version": "scaffold-2026-08-18",
        "content_hash": make_content_hash(prompt),
        "split": split,
    }


def test_public_development_row_rejects_forged_identity() -> None:
    row_data = _public_row_data()
    row_data["row_id"] = "row-" + "f" * 24

    with pytest.raises(ValidationError, match="row_id"):
        PublicDevelopmentRow.model_validate(row_data)


def test_public_development_row_rejects_forged_content_hash() -> None:
    row_data = _public_row_data()
    row_data["content_hash"] = "sha256:" + "f" * 64

    with pytest.raises(ValidationError, match="content_hash"):
        PublicDevelopmentRow.model_validate(row_data)
