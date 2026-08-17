from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter, sleep
from typing import Callable, Literal, Protocol

from .contracts import ModelRequest, ModelResponse
from .redaction import redact_text


class ProviderAdapter(Protocol):
    def generate(self, request: ModelRequest) -> ModelResponse:
        ...


class RetryableProviderError(RuntimeError):
    """Transport-level error that may be retried within the request budget."""


RemoteTransport = Callable[[ModelRequest], tuple[str, float]]


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
    provider: Literal["openai", "anthropic", "huggingface"]
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


@dataclass(frozen=True)
class GuardedRemoteProvider:
    """SDK-neutral remote adapter; transport injection keeps calls opt-in and testable."""

    provider: str
    model_id: str
    transport: RemoteTransport
    allow_remote: bool = False
    cost_ceiling: float = 0.0
    retry_base_seconds: float = 0.25

    def _not_run(self, request: ModelRequest, error_code: str) -> ModelResponse:
        return ModelResponse(
            request_hash=request.request_hash,
            row_id=request.row_id,
            provider=self.provider,
            model_id=self.model_id,
            status="not_run",
            error_code=error_code,
        )

    def generate(self, request: ModelRequest) -> ModelResponse:
        if request.provider != self.provider:
            raise ValueError("request provider does not match remote adapter")
        if not request.allow_remote or not self.allow_remote:
            return self._not_run(request, "remote_opt_in_required")
        if request.cost_ceiling <= 0 or self.cost_ceiling <= 0:
            return self._not_run(request, "cost_ceiling_required")
        if request.cost_ceiling > self.cost_ceiling:
            return self._not_run(request, "request_cost_ceiling_exceeds_adapter")

        started = perf_counter()
        attempts = 0
        while True:
            try:
                text, estimated_cost = self.transport(request)
                if not isinstance(text, str) or not text.strip():
                    return ModelResponse(
                        request_hash=request.request_hash,
                        row_id=request.row_id,
                        provider=self.provider,
                        model_id=self.model_id,
                        status="malformed",
                        text="Provider returned no usable text.",
                        latency_ms=(perf_counter() - started) * 1000,
                        cost_estimate=0.0,
                    )
                if estimated_cost < 0 or estimated_cost > request.cost_ceiling:
                    return ModelResponse(
                        request_hash=request.request_hash,
                        row_id=request.row_id,
                        provider=self.provider,
                        model_id=self.model_id,
                        status="provider_error",
                        error_code="cost_ceiling_exceeded",
                        latency_ms=(perf_counter() - started) * 1000,
                    )
                return ModelResponse(
                    request_hash=request.request_hash,
                    row_id=request.row_id,
                    provider=self.provider,
                    model_id=self.model_id,
                    status="complete",
                    text=redact_text(text),
                    latency_ms=(perf_counter() - started) * 1000,
                    cost_estimate=estimated_cost,
                )
            except (RetryableProviderError, TimeoutError):
                if attempts >= request.max_retries:
                    return ModelResponse(
                        request_hash=request.request_hash,
                        row_id=request.row_id,
                        provider=self.provider,
                        model_id=self.model_id,
                        status="timeout",
                        error_code="retry_budget_exhausted",
                        latency_ms=(perf_counter() - started) * 1000,
                    )
                sleep(min(self.retry_base_seconds * (2**attempts), 8.0))
                attempts += 1
            except Exception:
                return ModelResponse(
                    request_hash=request.request_hash,
                    row_id=request.row_id,
                    provider=self.provider,
                    model_id=self.model_id,
                    status="provider_error",
                    error_code="provider_error_redacted",
                    latency_ms=(perf_counter() - started) * 1000,
                )
