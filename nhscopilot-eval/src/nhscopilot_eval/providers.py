from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .contracts import ModelRequest, ModelResponse
from .redaction import redact_text


class ProviderAdapter(Protocol):
    def generate(self, request: ModelRequest) -> ModelResponse:
        ...


@dataclass(frozen=True)
class LocalFixtureProvider:
    model_id: str = "local-fixture-baseline"

    def generate(self, request: ModelRequest) -> ModelResponse:
        if request.provider != "local" or request.allow_remote:
            raise ValueError("fixture provider accepts local, non-remote requests only")
        text = redact_text(
            f"Fixture response for {request.category}; "
            "requires human review and does not establish clinical safety."
        )
        return ModelResponse(
            request_hash=request.request_hash,
            row_id=request.row_id,
            provider="local",
            model_id=self.model_id,
            status="complete",
            text=text,
            latency_ms=0.0,
            cost_estimate=0.0,
        )


@dataclass(frozen=True)
class UnavailableProvider:
    provider: str
    model_id: str
    error_code: str = "not_available"

    def generate(self, request: ModelRequest) -> ModelResponse:
        if request.provider != self.provider:
            raise ValueError("request provider does not match unavailable adapter")
        return ModelResponse(
            request_hash=request.request_hash,
            row_id=request.row_id,
            provider=self.provider,
            model_id=self.model_id,
            status="not_run",
            error_code=self.error_code,
        )
