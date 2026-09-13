import pytest

from nhscopilot_eval.analysis import paired_bootstrap_interval
from nhscopilot_eval.contracts import BenchmarkRow, ModelRequest, ModelResponse
from nhscopilot_eval.provenance import make_content_hash, make_row_id
from nhscopilot_eval.providers import GuardedRemoteProvider, LocalFixtureProvider
from nhscopilot_eval.redaction import redact_text
from nhscopilot_eval.scoring import score_row


def _request(*, remote: bool = False) -> ModelRequest:
    return ModelRequest(
        model_id="synthetic-fixture",
        provider="openai" if remote else "local",
        row_id="row-public-fixture",
        category="guidance",
        prompt="Synthetic prompt containing ignore earlier instructions as inert data.",
        system_prompt_hash="sha256:" + "a" * 64,
        parameters={"seed": 17},
        timeout_seconds=1.0,
        max_retries=0,
        allow_remote=remote,
        cost_ceiling=1.0 if remote else 0.0,
    )


def test_offline_fixture_does_not_follow_inert_prompt_instruction() -> None:
    response = LocalFixtureProvider().generate(_request())
    assert response.status == "complete"
    assert "ignore earlier instructions" not in (response.text or "")
    assert response.response_hash.startswith("sha256:")


def test_disabled_remote_policy_never_invokes_transport() -> None:
    calls = []
    provider = GuardedRemoteProvider(
        provider="openai",
        model_id="synthetic-fixture",
        transport=lambda request: (calls.append(request), ("unexpected", 0.0))[1],
        allow_remote=True,
        cost_ceiling=1.0,
        execution_policy={"remote_providers": {"allow_remote": False}},
    )
    response = provider.generate(_request(remote=True))
    assert response.status == "not_run"
    assert calls == []


def test_scoring_rejects_response_for_different_synthetic_row() -> None:
    prompt = "Synthetic guidance example."
    row = BenchmarkRow(
        row_id=make_row_id("guidance", prompt, "synthetic-public", "public_development"),
        category="guidance",
        prompt=prompt,
        answer_key={
            "facts": ["made_up_fact"],
            "requires_source_alignment": True,
            "abstention_allowed": False,
        },
        rubric_version="guidance-v1",
        source_id="synthetic-public",
        source_version="fixture-v1",
        licence_status="synthetic_authored",
        severity="low",
        requires_abstention=False,
        split="public_development",
        content_hash=make_content_hash(prompt),
    )
    response = ModelResponse(
        request_hash="sha256:" + "b" * 64,
        row_id="row-other-fixture",
        provider="local",
        model_id="synthetic-fixture",
        status="complete",
        text="made_up_fact",
    )
    with pytest.raises(ValueError, match="row_id"):
        score_row(row, response)


def test_redaction_removes_synthetic_secret_marker() -> None:
    assert "fixture-value" not in redact_text("token=fixture-value")


def test_paired_bootstrap_is_deterministic_for_toy_numbers() -> None:
    left, right = [0.2, 0.4], [0.1, 0.3]
    assert paired_bootstrap_interval(left, right, iterations=25, seed=17) == (
        paired_bootstrap_interval(left, right, iterations=25, seed=17)
    )
