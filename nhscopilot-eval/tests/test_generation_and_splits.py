from nhscopilot_eval.prompts import build_synthetic_rows, validate_target_counts
from nhscopilot_eval.splits import public_projection, validate_disjoint_rows


def test_synthetic_authoring_has_exact_category_targets() -> None:
    rows = build_synthetic_rows()

    assert len(rows) == 200
    assert validate_target_counts(rows) == {
        "guidance": 100,
        "icd10_synthetic": 50,
        "medication_safety": 50,
    }


def test_synthetic_splits_are_disjoint_and_public_projection_has_no_answer_key() -> None:
    rows = build_synthetic_rows()

    counts = validate_disjoint_rows(rows)
    assert counts == {
        "private_authoring": 50,
        "public_development": 100,
        "sealed_evaluation": 50,
    }
    projected = public_projection(next(row for row in rows if row.split == "public_development"))
    assert "answer_key" not in projected.model_dump()
