from __future__ import annotations

from typing import Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)

from .provenance import (
    canonical_json,
    make_content_hash,
    make_row_id,
    stable_hash,
)

Category = Literal["guidance", "icd10_synthetic", "medication_safety"]
Split = Literal["public_development", "private_authoring", "sealed_evaluation"]
ResponseStatus = Literal[
    "complete",
    "refusal",
    "abstention",
    "insufficient_information",
    "malformed",
    "timeout",
    "provider_error",
    "not_run",
]

STRICT_MODEL = ConfigDict(
    extra="forbid",
    strict=True,
    validate_assignment=True,
)


def _hash_field(value: str) -> str:
    if not value.startswith("sha256:") or len(value) != 71:
        raise ValueError("value must be a sha256-prefixed 64-character digest")
    int(value[7:], 16)
    return value


class SourceManifest(BaseModel):
    model_config = STRICT_MODEL

    source_id: str = Field(min_length=3, pattern=r"^[a-z0-9][a-z0-9_-]+$")
    source_type: Literal[
        "independently_authored_synthetic",
        "licence_cleared_external",
        "external_source",
    ]
    version: str = Field(min_length=1)
    url: HttpUrl | None = None
    licence_decision: Literal[
        "local_authorship_only",
        "licence_cleared",
        "pending",
        "blocked",
    ]
    ai_reuse_decision: Literal[
        "permitted_for_local_synthetic_development",
        "permitted",
        "pending",
        "denied",
    ]
    citation_anchor: str = Field(min_length=1)
    content_hash: str
    public_release: Literal[
        "blocked_until_disclosure_review",
        "permitted_after_review",
        "blocked",
    ]

    @field_validator("content_hash")
    @classmethod
    def validate_content_hash(cls, value: str) -> str:
        if value in {
            "not_applicable_no_rows_authored",
            "local_generated_artifact_not_released",
        }:
            return value
        return _hash_field(value)

    @model_validator(mode="after")
    def validate_rights_gate(self) -> SourceManifest:
        if self.source_type == "external_source":
            if self.url is None:
                raise ValueError("external sources require a canonical URL")
            if self.licence_decision != "licence_cleared":
                raise ValueError("external sources require a cleared licence decision")
            if self.ai_reuse_decision != "permitted":
                raise ValueError("external sources require an AI reuse decision")
            if self.content_hash == "not_applicable_no_rows_authored":
                raise ValueError("external sources require a content hash")
        if self.source_type == "independently_authored_synthetic":
            if self.url is not None:
                raise ValueError("synthetic sources must not carry an external URL")
            if self.licence_decision != "local_authorship_only":
                raise ValueError("synthetic sources require a local authorship decision")
        if self.public_release == "permitted_after_review" and self.source_type == "external_source":
            if self.licence_decision != "licence_cleared":
                raise ValueError("public external release requires a cleared licence")
        return self


class BenchmarkRow(BaseModel):
    model_config = STRICT_MODEL

    row_id: str = Field(min_length=5, pattern=r"^row-[a-z0-9][a-z0-9_-]+$")
    category: Category
    prompt: str = Field(min_length=1)
    answer_key: dict[str, Any] = Field(min_length=1)
    rubric_version: str = Field(min_length=1)
    source_id: str = Field(min_length=3, pattern=r"^[a-z0-9][a-z0-9_-]+$")
    source_version: str = Field(min_length=1)
    licence_status: Literal[
        "synthetic_authored",
        "licence_cleared",
        "private_review_required",
        "pending_rights_review",
        "blocked",
    ]
    severity: Literal["low", "medium", "high", "critical"]
    requires_abstention: bool
    split: Split
    content_hash: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("prompt must not be empty")
        return cleaned

    @field_validator("content_hash")
    @classmethod
    def validate_row_content_hash(cls, value: str) -> str:
        return _hash_field(value)

    @model_validator(mode="after")
    def validate_identity_and_rights(self) -> BenchmarkRow:
        expected_id = make_row_id(
            self.category,
            self.prompt,
            self.source_id,
            self.split,
        )
        if self.row_id != expected_id:
            raise ValueError("row_id does not match deterministic row identity")
        if self.content_hash != make_content_hash(self.prompt):
            raise ValueError("content_hash does not match the canonical prompt hash")
        if self.licence_status in {"pending_rights_review", "blocked"}:
            raise ValueError("rows cannot enter a benchmark with unresolved rights")
        return self


class ModelRequest(BaseModel):
    model_config = STRICT_MODEL

    model_id: str = Field(min_length=1)
    provider: Literal["local", "openai", "anthropic", "huggingface"]
    row_id: str = Field(min_length=5, pattern=r"^row-[a-z0-9][a-z0-9_-]+$")
    category: Category
    prompt: str = Field(min_length=1)
    system_prompt_hash: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: float = Field(gt=0, le=300)
    max_retries: int = Field(ge=0, le=5)
    allow_remote: bool
    cost_ceiling: float = Field(ge=0)
    request_hash: str | None = None

    @field_validator("prompt")
    @classmethod
    def validate_request_prompt(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("request prompt must not be empty")
        return cleaned

    @field_validator("system_prompt_hash")
    @classmethod
    def validate_system_prompt_hash(cls, value: str) -> str:
        return _hash_field(value)

    @model_validator(mode="after")
    def validate_remote_policy_and_hash(self) -> ModelRequest:
        if self.provider == "local" and self.allow_remote:
            raise ValueError("local requests cannot enable remote execution")
        if self.provider != "local" and not self.allow_remote:
            raise ValueError("remote providers require explicit opt-in")
        payload = self.model_dump(mode="json", exclude={"request_hash"})
        expected_hash = stable_hash(payload)
        if self.request_hash is not None and self.request_hash != expected_hash:
            raise ValueError("request_hash does not match request configuration")
        object.__setattr__(self, "request_hash", expected_hash)
        return self


class ModelResponse(BaseModel):
    model_config = STRICT_MODEL

    request_hash: str
    row_id: str = Field(min_length=5, pattern=r"^row-[a-z0-9][a-z0-9_-]+$")
    provider: Literal["local", "openai", "anthropic", "huggingface"]
    model_id: str = Field(min_length=1)
    status: ResponseStatus
    text: str | None = None
    error_code: str | None = None
    latency_ms: float | None = Field(default=None, ge=0)
    cost_estimate: float = Field(default=0.0, ge=0)
    response_hash: str | None = None

    @field_validator("request_hash")
    @classmethod
    def validate_request_hash(cls, value: str) -> str:
        return _hash_field(value)

    @model_validator(mode="after")
    def validate_response_state_and_hash(self) -> ModelResponse:
        text_required = {
            "complete",
            "refusal",
            "abstention",
            "insufficient_information",
            "malformed",
        }
        if self.status in text_required and not self.text:
            raise ValueError(f"{self.status} responses require redacted text")
        if self.status == "not_run":
            if self.text is not None:
                raise ValueError("not_run responses must not retain response text")
            if not self.error_code:
                raise ValueError("not_run responses require an availability error code")
        if self.status in {"timeout", "provider_error"} and self.text is not None:
            raise ValueError("failure responses must not retain response text")
        payload = self.model_dump(mode="json", exclude={"response_hash"})
        object.__setattr__(self, "response_hash", stable_hash(payload))
        return self


class PublicDevelopmentRow(BaseModel):
    model_config = STRICT_MODEL

    row_id: str = Field(min_length=5, pattern=r"^row-[a-z0-9][a-z0-9_-]+$")
    category: Category
    prompt: str = Field(min_length=1)
    source_id: str = Field(min_length=3, pattern=r"^[a-z0-9][a-z0-9_-]+$")
    source_version: str = Field(min_length=1)
    content_hash: str
    split: Literal["public_development"]

    @field_validator("content_hash")
    @classmethod
    def validate_public_content_hash(cls, value: str) -> str:
        return _hash_field(value)


class AggregateResult(BaseModel):
    model_config = STRICT_MODEL

    model_id: str = Field(min_length=1)
    model_version: str | None = None
    category: Category
    status: Literal["available", "not_run"]
    metrics: dict[str, float] = Field(default_factory=dict)
    uncertainty: dict[str, float] = Field(default_factory=dict)
    source_links: list[HttpUrl] = Field(default_factory=list)


class PublicBundle(BaseModel):
    model_config = STRICT_MODEL

    bundle_id: str = Field(min_length=1)
    schema_version: str = Field(min_length=1)
    generated_at: str = Field(min_length=1)
    development_rows: list[PublicDevelopmentRow] = Field(default_factory=list)
    aggregates: list[AggregateResult] = Field(default_factory=list)
    manifest_ids: list[str] = Field(default_factory=list)
    source_links: list[HttpUrl] = Field(default_factory=list)
    disclaimer: str = Field(min_length=1)

    @field_validator("disclaimer")
    @classmethod
    def validate_disclaimer(cls, value: str) -> str:
        lowered = value.casefold()
        if "not clinical advice" not in lowered:
            raise ValueError("public bundle requires a not-clinical-advice disclaimer")
        if "does not establish" not in lowered:
            raise ValueError("public bundle must not imply safety or compliance")
        return value


__all__ = [
    "AggregateResult",
    "BenchmarkRow",
    "ModelRequest",
    "ModelResponse",
    "PublicBundle",
    "PublicDevelopmentRow",
    "SourceManifest",
    "canonical_json",
    "make_content_hash",
    "make_row_id",
    "stable_hash",
]
