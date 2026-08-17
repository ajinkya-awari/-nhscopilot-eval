from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import AggregateResult, BenchmarkRow, PublicBundle
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
        disclaimer=DISCLAIMER,
    )


def write_public_bundle(bundle: PublicBundle, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(bundle.model_dump(mode="json"), indent=2, sort_keys=True),
        encoding="utf-8",
    )
