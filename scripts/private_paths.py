from __future__ import annotations

from pathlib import Path


PRIVATE_OUTPUT_ROOT = Path("data/private")


def validate_private_output_path(path: Path) -> Path:
    root = PRIVATE_OUTPUT_ROOT.resolve()
    resolved = Path(path).resolve()
    if resolved == root or root not in resolved.parents:
        raise ValueError("private output must remain under data/private")
    return resolved
