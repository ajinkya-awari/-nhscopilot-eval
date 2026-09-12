from __future__ import annotations

import argparse
import json
from pathlib import Path

from nhscopilot_eval.contracts import ModelRequest
from nhscopilot_eval.providers import LocalFixtureProvider, UnavailableProvider

if __package__:
    from .private_paths import validate_private_output_path
else:
    from private_paths import validate_private_output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a local fixture or not_run evaluation.")
    parser.add_argument("--mode", choices=("fixture", "not_run"), default="not_run")
    parser.add_argument("--output", type=Path, default=Path("data/private/results.jsonl"))
    args = parser.parse_args()
    output_path = validate_private_output_path(args.output)

    request = ModelRequest(
        model_id="local-fixture-baseline",
        provider="local",
        row_id="row-evaluation-fixture",
        category="guidance",
        prompt="Synthetic evaluation fixture only.",
        system_prompt_hash="sha256:" + "d" * 64,
        parameters={"temperature": 0.0, "seed": 17},
        timeout_seconds=30.0,
        max_retries=0,
        allow_remote=False,
        cost_ceiling=0.0,
    )
    provider = (
        LocalFixtureProvider()
        if args.mode == "fixture"
        else UnavailableProvider(provider="local", model_id="local-fixture-baseline")
    )
    response = provider.generate(request)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(response.model_dump(mode="json")) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
