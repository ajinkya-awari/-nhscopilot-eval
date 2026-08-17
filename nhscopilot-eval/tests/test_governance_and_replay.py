from pathlib import Path

import pytest
from pydantic import ValidationError

from nhscopilot_eval.adjudication import ReviewRecord, adjudicate_reviews
from nhscopilot_eval.replay import ReplayRecord
from nhscopilot_eval.sources import load_yaml, validate_synthetic_fallback_manifest


def test_local_source_manifest_stays_synthetic_only() -> None:
    path = Path("configs/source_manifest.yaml")
    validate_synthetic_fallback_manifest(load_yaml(path))


def test_adjudication_requires_independent_reviews() -> None:
    reviews = [
        ReviewRecord(
            row_id="row-review-fixture",
            reviewer_id="reviewer-a",
            outcome="accept",
            severity="high",
            notes="synthetic review one",
        ),
        ReviewRecord(
            row_id="row-review-fixture",
            reviewer_id="reviewer-b",
            outcome="accept",
            severity="high",
            notes="synthetic review two",
        ),
    ]

    result = adjudicate_reviews(reviews)

    assert result.outcome == "accept"
    assert result.reviewer_ids == ["reviewer-a", "reviewer-b"]


def test_adjudication_rejects_one_reviewer() -> None:
    review = ReviewRecord(
        row_id="row-review-fixture",
        reviewer_id="reviewer-a",
        outcome="accept",
        severity="high",
        notes="synthetic review",
    )

    with pytest.raises(ValueError):
        adjudicate_reviews([review])


def test_replay_record_contains_hashes_not_raw_payloads() -> None:
    record = ReplayRecord.from_payload(
        row_id="row-replay-fixture",
        model_id="local-fixture-baseline",
        provider="local",
        request_payload={"prompt": "synthetic"},
        response_hash="sha256:" + "f" * 64,
        configuration_payload={"temperature": 0.0},
        source_manifest_payload={"manifest_id": "synthetic"},
        status="complete",
    )

    assert record.request_hash.startswith("sha256:")
    assert "synthetic" not in record.request_hash
    assert "prompt" not in record.model_dump()


def test_replay_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ReplayRecord(
            row_id="row-replay-fixture",
            model_id="local-fixture-baseline",
            provider="local",
            request_hash="sha256:" + "a" * 64,
            configuration_hash="sha256:" + "b" * 64,
            source_manifest_hash="sha256:" + "c" * 64,
            status="not_run",
            raw_output="forbidden",
        )
