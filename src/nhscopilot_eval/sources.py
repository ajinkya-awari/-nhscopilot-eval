from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .contracts import SourceManifest


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected a mapping in {path}")
    return data


def validate_synthetic_fallback_manifest(data: dict[str, Any]) -> None:
    if data.get("status") != "synthetic_fallback_only":
        raise ValueError("source manifest must remain synthetic-only until rights review")
    if data.get("external_sources") != []:
        raise ValueError("external source entries are not admitted in the fallback manifest")
    synthetic_sources = data.get("synthetic_sources")
    if not isinstance(synthetic_sources, list) or not synthetic_sources:
        raise ValueError("synthetic fallback requires typed synthetic source entries")
    for entry in synthetic_sources:
        source = SourceManifest.model_validate(entry)
        if source.source_type != "independently_authored_synthetic":
            raise ValueError("fallback source entries must be independently authored synthetic")
    if data.get("rights_gate", {}).get("bnf") != "excluded":
        raise ValueError("BNF must remain excluded")
    if data.get("rights_gate", {}).get("restricted_source_text") != "not_present":
        raise ValueError("restricted source text must be absent")
