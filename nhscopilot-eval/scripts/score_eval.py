from __future__ import annotations

import argparse
import json
from pathlib import Path

from nhscopilot_eval.contracts import BenchmarkRow, ModelResponse
from nhscopilot_eval.scoring import score_row


def main() -> int:
    parser = argparse.ArgumentParser(description="Score private synthetic evaluation records.")
    parser.add_argument("rows", type=Path)
    parser.add_argument("responses", type=Path)
    parser.add_argument("--output", type=Path, default=Path("artifacts/private/scores.jsonl"))
    args = parser.parse_args()

    rows = {
        row.row_id: row
        for row in (
            BenchmarkRow.model_validate(json.loads(line))
            for line in args.rows.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    responses = (
        ModelResponse.model_validate(json.loads(line))
        for line in args.responses.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    scores = []
    for response in responses:
        row_id = response.row_id
        if row_id in rows:
            scores.append(score_row(rows[row_id], response))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(score, sort_keys=True) + "\n" for score in scores),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
