from __future__ import annotations

import argparse
import json
from pathlib import Path

from nhscopilot_eval.prompts import build_synthetic_rows, validate_target_counts
from nhscopilot_eval.splits import public_projection, validate_disjoint_rows


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build synthetic Project 09 rows.")
    parser.add_argument("--private-output", type=Path, default=Path("data/private/benchmark.jsonl"))
    parser.add_argument("--public-output", type=Path, default=Path("data/public/benchmark_metadata.jsonl"))
    args = parser.parse_args()

    rows = build_synthetic_rows()
    validate_target_counts(rows)
    validate_disjoint_rows(rows)
    write_jsonl(
        args.private_output,
        [row.model_dump(mode="json") for row in rows],
    )
    write_jsonl(
        args.public_output,
        [public_projection(row).model_dump(mode="json") for row in rows if row.split == "public_development"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
