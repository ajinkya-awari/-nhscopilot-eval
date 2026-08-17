from __future__ import annotations

from collections.abc import Iterable

from .contracts import BenchmarkRow
from .provenance import make_content_hash, make_row_id

SOURCE_ID = "synthetic-authored-project09"
SOURCE_VERSION = "synthetic-scaffold-2026-08-18"


def _split(category: str, index: int) -> str:
    public_limits = {"guidance": 50, "icd10_synthetic": 25, "medication_safety": 25}
    private_limits = {"guidance": 75, "icd10_synthetic": 38, "medication_safety": 38}
    if index < public_limits[category]:
        return "public_development"
    if index < private_limits[category]:
        return "private_authoring"
    return "sealed_evaluation"


def _prompt(category: str, index: int) -> tuple[str, dict[str, object], str]:
    if category == "guidance":
        prompt = (
            f"Synthetic guidance task {index + 1}: state one supported action, "
            "one uncertainty, and whether escalation is needed."
        )
        answer = {
            "facts": [f"synthetic_action_{index + 1}"],
            "requires_source_alignment": True,
            "abstention_allowed": index % 10 == 0,
        }
        rubric = "guidance-v1"
    elif category == "icd10_synthetic":
        prompt = (
            f"Synthetic coding vignette {index + 1}: return the two supplied "
            "placeholder coding labels without inventing additional labels."
        )
        answer = {
            "codes": [f"S{index % 9 + 1:02d}.{index % 4}", f"T{index % 8 + 1:02d}"],
            "primary_code": f"S{index % 9 + 1:02d}.{index % 4}",
            "insufficient_information": index % 11 == 0,
        }
        rubric = "icd10-synthetic-v1"
    else:
        prompt = (
            f"Synthetic medication-safety scenario {index + 1}: classify the "
            "communication as safe, unsafe, review, or insufficient-information."
        )
        outcomes = ("safe", "unsafe", "review", "insufficient_information")
        answer = {
            "outcome": outcomes[index % len(outcomes)],
            "severity": ("low", "medium", "high", "critical")[index % 4],
            "requires_abstention": index % 7 == 0,
        }
        rubric = "medication-safety-v1"
    return prompt, answer, rubric


def build_synthetic_rows() -> list[BenchmarkRow]:
    rows: list[BenchmarkRow] = []
    for category, count in (
        ("guidance", 100),
        ("icd10_synthetic", 50),
        ("medication_safety", 50),
    ):
        for index in range(count):
            prompt, answer_key, rubric = _prompt(category, index)
            split = _split(category, index)
            severity = (
                answer_key.get("severity", "low")
                if category == "medication_safety"
                else ("medium" if index % 9 == 0 else "low")
            )
            row_id = make_row_id(category, prompt, SOURCE_ID, split)
            rows.append(
                BenchmarkRow(
                    row_id=row_id,
                    category=category,
                    prompt=prompt,
                    answer_key=answer_key,
                    rubric_version=rubric,
                    source_id=SOURCE_ID,
                    source_version=SOURCE_VERSION,
                    licence_status="synthetic_authored",
                    severity=severity,
                    requires_abstention=bool(answer_key.get("requires_abstention", False)),
                    split=split,
                    content_hash=make_content_hash(prompt),
                )
            )
    return rows


def validate_target_counts(rows: Iterable[BenchmarkRow]) -> dict[str, int]:
    counts = {"guidance": 0, "icd10_synthetic": 0, "medication_safety": 0}
    for row in rows:
        counts[row.category] += 1
    expected = {"guidance": 100, "icd10_synthetic": 50, "medication_safety": 50}
    if counts != expected:
        raise ValueError(f"unexpected category counts: {counts}")
    return counts
