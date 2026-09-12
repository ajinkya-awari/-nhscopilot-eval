from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import (
    PUBLIC_SYNTHETIC_SOURCE_ID,
    PUBLIC_SYNTHETIC_SOURCE_VERSION,
    AggregateResult,
    BenchmarkRow,
    PublicBundle,
)
from .splits import public_projection

DISCLAIMER = (
    "Research evaluation only; not clinical advice and does not establish "
    "clinical safety, regulatory compliance, or institutional endorsement."
)


def build_public_bundle(
    rows: list[BenchmarkRow],
    aggregates: list[AggregateResult],
    *,
    generated_at: str,
) -> PublicBundle:
    if any(aggregate.status == "available" for aggregate in aggregates):
        raise ValueError("available aggregates require a verified release evidence gate")
    if any(
        row.licence_status != "synthetic_authored"
        or row.source_id != PUBLIC_SYNTHETIC_SOURCE_ID
        or row.source_version != PUBLIC_SYNTHETIC_SOURCE_VERSION
        for row in rows
    ):
        raise ValueError("public bundle currently admits synthetic-authored rows only")
    return PublicBundle(
        bundle_id="project09-aggregate-bundle",
        schema_version="0.1",
        generated_at=generated_at,
        development_rows=[
            public_projection(row)
            for row in rows
            if row.split == "public_development"
        ],
        aggregates=aggregates,
        manifest_ids=["project09-source-manifest-scaffold"],
        source_links=[],
        disclaimer=DISCLAIMER,
    )


def write_public_bundle(bundle: PublicBundle, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(bundle.model_dump(mode="json"), indent=2, sort_keys=True),
        encoding="utf-8",
    )
