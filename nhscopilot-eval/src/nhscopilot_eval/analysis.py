from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Iterable, Sequence
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
    rng = random.Random(seed)
    paired = list(zip(left, right, strict=True))
    differences = []
    for _ in range(iterations):
        sample = [rng.choice(paired) for _ in paired]
        differences.append(mean(a - b for a, b in sample))
    differences.sort()
    low = differences[max(0, int(iterations * 0.025) - 1)]
    high = differences[min(iterations - 1, int(iterations * 0.975))]
    return {"estimate": mean(left) - mean(right), "low": low, "high": high}


def aggregate_category_scores(
    scored_rows: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for result in scored_rows:
        if result.get("scored") and isinstance(result.get("metric"), (int, float)):
            buckets[str(result["category"])].append(float(result["metric"]))
    return [
        {
            "category": category,
            "count": len(values),
            "mean": mean(values),
        }
        for category, values in sorted(buckets.items())
    ]
