from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .provenance import stable_hash


def _validate_hash(value: str) -> str:
    if not value.startswith("sha256:") or len(value) != 71:
        raise ValueError("value must be a sha256-prefixed 64-character digest")
    int(value[7:], 16)
    return value


class ReplayRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    row_id: str = Field(min_length=5)
    model_id: str = Field(min_length=1)
    provider: Literal["local", "openai", "anthropic", "huggingface"]
    request_hash: str
    response_hash: str | None = None
    configuration_hash: str
    source_manifest_hash: str
    status: Literal["complete", "not_run", "error"]

    @field_validator("request_hash")
    @classmethod
    def validate_request_hash(cls, value: str) -> str:
        return _validate_hash(value)

    @field_validator("configuration_hash")
    @classmethod
    def validate_configuration_hash(cls, value: str) -> str:
        return _validate_hash(value)

    @field_validator("source_manifest_hash")
    @classmethod
    def validate_source_manifest_hash(cls, value: str) -> str:
        return _validate_hash(value)

    @field_validator("response_hash")
    @classmethod
    def validate_response_hash(cls, value: str | None) -> str | None:
        return None if value is None else _validate_hash(value)

    @model_validator(mode="after")
    def require_complete_response_hash(self) -> "ReplayRecord":
        if self.status == "complete" and self.response_hash is None:
            raise ValueError("complete replay records require a response_hash")
        return self

    @classmethod
    def from_payload(
        cls,
        *,
        row_id: str,
        model_id: str,
        provider: Literal["local", "openai", "anthropic", "huggingface"],
        request_payload: object,
        response_hash: str | None,
        configuration_payload: object,
        source_manifest_payload: object,
        status: Literal["complete", "not_run", "error"],
    ) -> "ReplayRecord":
        return cls(
            row_id=row_id,
            model_id=model_id,
            provider=provider,
            request_hash=stable_hash(request_payload),
            response_hash=response_hash,
            configuration_hash=stable_hash(configuration_payload),
            source_manifest_hash=stable_hash(source_manifest_payload),
            status=status,
        )
