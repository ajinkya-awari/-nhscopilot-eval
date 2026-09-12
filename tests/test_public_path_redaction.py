from pathlib import Path

import pytest

from scripts.private_paths import PRIVATE_OUTPUT_ROOT, validate_private_output_path


def test_rejected_output_path_does_not_reveal_private_absolute_root() -> None:
    with pytest.raises(ValueError, match="private output") as error:
        validate_private_output_path(Path("artifacts/public/results.jsonl"))

    assert str(PRIVATE_OUTPUT_ROOT.resolve()) not in str(error.value)
