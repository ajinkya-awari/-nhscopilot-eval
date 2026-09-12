import math

import pytest

from nhscopilot_eval.analysis import aggregate_category_scores


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_aggregate_rejects_nonfinite_scored_metric(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        aggregate_category_scores(
            [{"category": "guidance", "status": "complete", "scored": True, "metric": value}]
        )
