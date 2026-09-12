"""Synthetic-only offline contract example. No provider or model is called."""

import json

from nhscopilot_eval.contracts import ModelRequest
from nhscopilot_eval.providers import LocalFixtureProvider


def main() -> None:
    request = ModelRequest(
        model_id="local-fixture-baseline",
        provider="local",
        row_id="row-public-fixture",
        category="guidance",
        prompt="Synthetic fixture: summarize a made-up evidence label.",
        system_prompt_hash="sha256:" + "a" * 64,
        parameters={"temperature": 0.0, "seed": 17},
        timeout_seconds=5.0,
        max_retries=0,
        allow_remote=False,
        cost_ceiling=0.0,
    )
    response = LocalFixtureProvider().generate(request)
    print(
        json.dumps(
            {
                "mode": "synthetic_offline_fixture",
                "status": response.status,
                "request_hash": request.request_hash,
                "response_hash": response.response_hash,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
