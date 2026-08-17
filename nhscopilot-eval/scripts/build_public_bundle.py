from __future__ import annotations

import argparse
import json
from pathlib import Path

from nhscopilot_eval.contracts import AggregateResult, BenchmarkRow
from nhscopilot_eval.report import build_public_bundle, write_public_bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an aggregate-only public bundle.")
    parser.add_argument("rows", type=Path)
    parser.add_argument("aggregates", type=Path)
    parser.add_argument("--output", type=Path, default=Path("artifacts/public_bundle/manifest.json"))
    parser.add_argument("--generated-at", required=True)
    args = parser.parse_args()

    rows = [
        BenchmarkRow.model_validate(json.loads(line))
        for line in args.rows.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    aggregates = [
        AggregateResult.model_validate(record)
        for record in json.loads(args.aggregates.read_text(encoding="utf-8"))
    ]
    write_public_bundle(
        build_public_bundle(rows, aggregates, generated_at=args.generated_at),
        args.output,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
