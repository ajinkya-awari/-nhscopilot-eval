from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .provenance import stable_hash


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
