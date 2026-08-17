from __future__ import annotations

import pytest
from pydantic import ValidationError

from nhscopilot_eval.contracts import (
    BenchmarkRow,
    ModelRequest,
    ModelResponse,
    PublicBundle,
    SourceManifest,
    canonical_json,
    make_content_hash,
    make_row_id,
    stable_hash,
)


def valid_source_manifest() -> SourceManifest:
    return SourceManifest(
        source_id="synthetic-authored-project09",
        source_type="independently_authored_synthetic",
        version="fixture-2026-08-18",
        licence_decision="local_authorship_only",
        ai_reuse_decision="permitted_for_local_synthetic_development",
        citation_anchor="none",
        content_hash="not_applicable_no_rows_authored",
        public_release="blocked_until_disclosure_review",
    )


def valid_row_data() -> dict[str, object]:
    category = "guidance"
    prompt = "Synthetic participant A asks for a concise evidence-summary response."
    source_id = "synthetic-authored-project09"
    split = "private_authoring"
    return {
        "row_id": make_row_id(category, prompt, source_id, split),
        "category": category,
        "prompt": prompt,
        "answer_key": {"facts": ["synthetic fact one"], "abstention": False},
        "rubric_version": "guidance-v1",
        "source_id": source_id,
        "source_version": "fixture-2026-08-18",
        "licence_status": "synthetic_authored",
        "severity": "low",
        "requires_abstention": False,
        "split": split,
        "content_hash": make_content_hash(prompt),
    }


def test_synthetic_source_manifest_accepts_local_fallback() -> None:
    manifest = valid_source_manifest()

    assert manifest.source_type == "independently_authored_synthetic"
    assert manifest.url is None
    assert manifest.public_release == "blocked_until_disclosure_review"


def test_canonical_json_and_hash_are_order_independent() -> None:
    left = {"b": 2, "a": ["x", 1]}
    right = {"a": ["x", 1], "b": 2}

    assert canonical_json(left) == canonical_json(right)
    assert stable_hash(left) == stable_hash(right)
    assert stable_hash(left).startswith("sha256:")


def test_benchmark_row_accepts_a_deterministic_identity() -> None:
    row = BenchmarkRow.model_validate(valid_row_data())

    assert row.row_id == make_row_id(row.category, row.prompt, row.source_id, row.split)
    assert row.content_hash == make_content_hash(row.prompt)


def test_benchmark_row_rejects_an_unknown_field() -> None:
    data = valid_row_data()
    data["unexpected"] = "must fail"

    with pytest.raises(ValidationError):
        BenchmarkRow.model_validate(data)


def test_benchmark_row_rejects_empty_prompt() -> None:
    data = valid_row_data()
    data["prompt"] = "  "

    with pytest.raises(ValidationError):
        BenchmarkRow.model_validate(data)


def test_benchmark_row_rejects_pending_rights() -> None:
    data = valid_row_data()
    data["licence_status"] = "pending_rights_review"

    with pytest.raises(ValidationError):
        BenchmarkRow.model_validate(data)


def test_source_manifest_rejects_external_content_without_rights() -> None:
    with pytest.raises(ValidationError):
        SourceManifest(
            source_id="external-unreviewed",
            source_type="external_source",
            version="unknown",
            licence_decision="pending",
            ai_reuse_decision="pending",
            citation_anchor="none",
            content_hash="not_recorded",
            public_release="blocked",
        )


def test_model_request_hash_is_stable_and_credential_free() -> None:
    request = ModelRequest(
        model_id="local-baseline-fixture",
        provider="local",
        row_id="row-guidance-fixture",
        category="guidance",
        prompt="Synthetic prompt only.",
        system_prompt_hash="sha256:" + "a" * 64,
        parameters={"temperature": 0.0, "seed": 7},
        timeout_seconds=30.0,
        max_retries=0,
        allow_remote=False,
        cost_ceiling=0.0,
    )
    repeated = ModelRequest.model_validate(request.model_dump())

    assert request.request_hash == repeated.request_hash
    assert "api_key" not in request.request_hash


def test_model_response_rejects_text_for_not_run() -> None:
    with pytest.raises(ValidationError):
        ModelResponse(
            request_hash="sha256:" + "b" * 64,
            row_id="row-response-fixture",
            provider="local",
            model_id="unavailable-fixture",
            status="not_run",
            text="must not be retained for an unavailable model",
            error_code="unavailable",
        )


def test_public_bundle_rejects_hidden_answer_key() -> None:
    with pytest.raises(ValidationError):
        PublicBundle(
            bundle_id="bundle-fixture",
            schema_version="0.1",
            generated_at="2026-08-18T00:00:00Z",
            development_rows=[
                {
                    "row_id": "row-guidance-fixture",
                    "category": "guidance",
                    "prompt": "Synthetic public development prompt.",
                    "source_id": "synthetic-authored-project09",
                    "source_version": "fixture-2026-08-18",
                    "content_hash": "sha256:" + "c" * 64,
                    "split": "public_development",
                    "answer_key": {"hidden": True},
                }
            ],
            aggregates=[],
            manifest_ids=["project09-source-manifest-scaffold"],
            disclaimer=(
                "Research evaluation only; not clinical advice and does not establish "
                "clinical safety or regulatory compliance."
            ),
        )


def test_public_bundle_requires_research_disclaimer() -> None:
    with pytest.raises(ValidationError):
        PublicBundle(
            bundle_id="bundle-fixture",
            schema_version="0.1",
            generated_at="2026-08-18T00:00:00Z",
            development_rows=[],
            aggregates=[],
            manifest_ids=[],
            disclaimer="Model results.",
        )
