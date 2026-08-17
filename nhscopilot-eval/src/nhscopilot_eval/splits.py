from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from .contracts import BenchmarkRow, PublicDevelopmentRow


def validate_disjoint_rows(rows: Iterable[BenchmarkRow]) -> dict[str, int]:
    materialized = list(rows)
    ids = [row.row_id for row in materialized]
    if len(ids) != len(set(ids)):
        raise ValueError("row IDs overlap")
    split_counts = Counter(row.split for row in materialized)
    if set(split_counts) != {
        "public_development",
        "private_authoring",
        "sealed_evaluation",
    }:
        raise ValueError("all three split boundaries must be present")
    return dict(sorted(split_counts.items()))


def public_projection(row: BenchmarkRow) -> PublicDevelopmentRow:
    if row.split != "public_development":
        raise ValueError("only public development rows may be projected")
    return PublicDevelopmentRow(
        row_id=row.row_id,
        category=row.category,
        prompt=row.prompt,
        source_id=row.source_id,
        source_version=row.source_version,
        content_hash=row.content_hash,
        split="public_development",
    )
