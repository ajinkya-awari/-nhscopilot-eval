from nhscopilot_eval.contracts import ModelRequest, ModelResponse
from nhscopilot_eval.providers import LocalFixtureProvider, UnavailableProvider
from nhscopilot_eval.prompts import build_synthetic_rows
from nhscopilot_eval.redaction import redact_text
from nhscopilot_eval.scoring import score_row


def local_request() -> ModelRequest:
    return ModelRequest(
        model_id="local-fixture-baseline",
        provider="local",
        row_id="row-provider-fixture",
        category="guidance",
        prompt="Synthetic provider fixture.",
        system_prompt_hash="sha256:" + "e" * 64,
        parameters={"temperature": 0.0},
        timeout_seconds=10.0,
        max_retries=0,
        allow_remote=False,
        cost_ceiling=0.0,
    )


def test_fixture_provider_returns_a_redacted_local_response() -> None:
    response = LocalFixtureProvider().generate(local_request())

    assert response.status == "complete"
    assert response.provider == "local"
    assert "clinical safety" in response.text


def test_unavailable_provider_is_not_run() -> None:
    request = local_request()
    response = UnavailableProvider(provider="local", model_id="missing").generate(request)

    assert response.status == "not_run"
    assert response.text is None


def test_redaction_removes_secret_and_identifier_markers() -> None:
    redacted = redact_text("token" + "=secret-value PERSON_001")

    assert "secret-value" not in redacted
    assert "PERSON_001" not in redacted


def test_scoring_dispatches_by_category() -> None:
    row = build_synthetic_rows()[0]
    response = LocalFixtureProvider().generate(local_request())

    result = score_row(row, response)

    assert result["category"] == "guidance"
    assert result["row_id"] == row.row_id
