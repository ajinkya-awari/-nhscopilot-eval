from pathlib import Path

from nhscopilot_eval.analysis import paired_bootstrap_interval
from nhscopilot_eval.app import export_static_catalogue
from nhscopilot_eval.contracts import AggregateResult
from nhscopilot_eval.prompts import build_synthetic_rows
from nhscopilot_eval.report import build_public_bundle


def test_paired_bootstrap_is_reproducible() -> None:
    left = [0.2, 0.4, 0.6]
    right = [0.1, 0.3, 0.5]

    assert paired_bootstrap_interval(left, right, iterations=100) == paired_bootstrap_interval(
        left, right, iterations=100
    )


def test_public_bundle_and_static_catalogue_exclude_hidden_rows(tmp_path: Path) -> None:
    bundle = build_public_bundle(
        build_synthetic_rows(),
        [
            AggregateResult(
                model_id="local-fixture-baseline",
                category="guidance",
                status="not_run",
                metrics={},
                uncertainty={},
            )
        ],
        generated_at="2026-08-18T00:00:00Z",
    )
    output = tmp_path / "leaderboard.html"
    export_static_catalogue(bundle, output)

    html = output.read_text(encoding="utf-8")
    assert "not clinical advice" in html
    assert "answer_key" not in html
