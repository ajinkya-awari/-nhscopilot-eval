from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from statistics import mean
from typing import Any


def paired_bootstrap_interval(
    left: Sequence[float],
    right: Sequence[float],
    *,
    iterations: int = 1000,
    seed: int = 17,
) -> dict[str, float]:
    if len(left) != len(right) or not left:
        raise ValueError("paired bootstrap requires equal non-empty sequences")
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations < 1:
        raise ValueError("iterations must be a positive integer")
    rng = random.Random(seed)
    paired = list(zip(left, right, strict=True))
    differences = []
    for _ in range(iterations):
        sample = [rng.choice(paired) for _ in paired]
        differences.append(mean(a - b for a, b in sample))
    differences.sort()
    low = differences[int((iterations - 1) * 0.025)]
    high = differences[int((iterations - 1) * 0.975)]
    return {"estimate": mean(left) - mean(right), "low": low, "high": high}


def build_paired_bootstrap_report(
    comparisons: Mapping[str, tuple[Sequence[float], Sequence[float]]],
    *,
    iterations: int = 1000,
    seed: int = 17,
) -> dict[str, Any]:
    """Build a reproducible, metadata-bearing CI report from paired metrics."""
    if not comparisons:
        raise ValueError("at least one paired comparison is required")
    for name, (left, right) in comparisons.items():
        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
            for value in (*left, *right)
        ):
            raise ValueError(f"comparison {name!r} contains a non-finite metric")
    return {
        "method": "paired_bootstrap_percentile",
        "confidence_level": 0.95,
        "iterations": iterations,
        "seed": seed,
        "comparisons": {
            name: {
                "n": len(left),
                **paired_bootstrap_interval(
                    left, right, iterations=iterations, seed=seed
                ),
            }
            for name, (left, right) in comparisons.items()
        },
    }


def write_paired_bootstrap_report(report: Mapping[str, Any], path: Path) -> None:
    """Persist only the caller-supplied sanitized numeric report structure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def aggregate_category_scores(
    scored_rows: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    buckets: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"values": [], "statuses": Counter()}
    )
    for result in scored_rows:
        category = str(result["category"])
        status = str(result.get("status", "unknown"))
        buckets[category]["statuses"][status] += 1
        if result.get("scored") and isinstance(result.get("metric"), (int, float)):
            metric = float(result["metric"])
            if not math.isfinite(metric):
                raise ValueError("scored metric must be finite")
            buckets[category]["values"].append(metric)
    failure_statuses = {"malformed", "timeout", "provider_error"}
    return [
        {
            "category": category,
            "count": len(bucket["values"]),
            "mean": mean(bucket["values"]) if bucket["values"] else None,
            "total_count": sum(bucket["statuses"].values()),
            "scored_count": len(bucket["values"]),
            "unscored_count": sum(bucket["statuses"].values()) - len(bucket["values"]),
            "not_run_count": bucket["statuses"].get("not_run", 0),
            "failure_count": sum(
                count
                for status, count in bucket["statuses"].items()
                if status in failure_statuses
            ),
            "status_counts": dict(sorted(bucket["statuses"].items())),
        }
        for category, bucket in sorted(buckets.items())
    ]
