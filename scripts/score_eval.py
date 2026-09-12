from __future__ import annotations

import argparse
import json
from collections.abc import Iterable, Mapping
from pathlib import Path

from nhscopilot_eval.contracts import BenchmarkRow, ModelResponse
from nhscopilot_eval.scoring import score_row

if __package__:
    from .private_paths import validate_private_output_path
else:
    from private_paths import validate_private_output_path


def score_responses(
    rows: Mapping[str, BenchmarkRow],
    responses: Iterable[ModelResponse],
) -> list[dict[str, object]]:
    scores: list[dict[str, object]] = []
    for response in responses:
        row = rows.get(response.row_id)
        if row is None:
            raise ValueError(f"unknown response row_id: {response.row_id}")
        scores.append(score_row(row, response))
    return scores


def main() -> int:
    parser = argparse.ArgumentParser(description="Score private synthetic evaluation records.")
    parser.add_argument("rows", type=Path)
    parser.add_argument("responses", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/private/scores.jsonl"))
    args = parser.parse_args()
    output_path = validate_private_output_path(args.output)

    rows: dict[str, BenchmarkRow] = {}
    for line in args.rows.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = BenchmarkRow.model_validate(json.loads(line))
        if row.row_id in rows:
            raise ValueError(f"duplicate row_id in rows input: {row.row_id}")
        rows[row.row_id] = row
    responses = (
        ModelResponse.model_validate(json.loads(line))
        for line in args.responses.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    scores = score_responses(rows, responses)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "".join(json.dumps(score, sort_keys=True) + "\n" for score in scores),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
