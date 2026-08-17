from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel


def _jsonable(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _jsonable(value.model_dump(mode="json", exclude_none=True))
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_jsonable(item) for item in value]
    return value


def canonical_json(value: Any) -> str:
    """Return deterministic JSON for hashes and replay metadata."""

    return json.dumps(
        _jsonable(value),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def stable_hash(value: Any) -> str:
    """Hash canonical JSON without retaining secrets or raw logs."""

    digest = hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def make_content_hash(prompt: str) -> str:
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    return stable_hash({"prompt": prompt.strip()})


def make_row_id(category: str, prompt: str, source_id: str, split: str) -> str:
    values = {
        "category": category.strip(),
        "prompt": prompt.strip(),
        "source_id": source_id.strip(),
        "split": split.strip(),
    }
    if any(not isinstance(value, str) or not value for value in values.values()):
        raise ValueError("row identity values must be non-empty strings")
    digest = stable_hash(values).removeprefix("sha256:")
    return f"row-{digest[:24]}"
