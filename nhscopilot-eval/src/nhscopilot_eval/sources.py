from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


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
    if data.get("rights_gate", {}).get("bnf") != "excluded":
        raise ValueError("BNF must remain excluded")
    if data.get("rights_gate", {}).get("restricted_source_text") != "not_present":
        raise ValueError("restricted source text must be absent")
