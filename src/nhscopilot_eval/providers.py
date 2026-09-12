from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import dataclass
from math import isfinite
from random import uniform
from time import perf_counter, sleep
from typing import Callable, Literal, Mapping, Protocol

from .contracts import ModelRequest, ModelResponse
from .redaction import redact_text


class ProviderAdapter(Protocol):
    def generate(self, request: ModelRequest) -> ModelResponse:
        ...


class RetryableProviderError(RuntimeError):
    """Transport-level error that may be retried within the request budget."""

    def __init__(
        self,
        message: str = "retryable provider error",
        *,
        error_code: str = "retryable_provider_error",
        retry_after_seconds: float | None = None,
    ) -> None:
        super().__init__(message)
        if retry_after_seconds is not None and retry_after_seconds < 0:
            raise ValueError("retry_after_seconds must not be negative")
        self.error_code = error_code
        self.retry_after_seconds = retry_after_seconds


RemoteTransport = Callable[[ModelRequest], tuple[str, float]]
SleepFunction = Callable[[float], None]
JitterFunction = Callable[[float], float]
PUBLIC_RETRY_ERROR_CODES = frozenset({
    "retryable_provider_error",
    "rate_limited",
    "server_error",
    "service_unavailable",
})


def _default_jitter(maximum_seconds: float) -> float:
    return uniform(0.0, maximum_seconds)


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
    provider: Literal["local", "openai", "anthropic", "huggingface"]
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
    execution_policy: Mapping[str, object] | None = None
    retry_base_seconds: float = 0.25
    max_backoff_seconds: float = 8.0
    sleep_fn: SleepFunction = sleep
    jitter_fn: JitterFunction = _default_jitter

    def _not_run(self, request: ModelRequest, error_code: str) -> ModelResponse:
        return ModelResponse(
            request_hash=request.request_hash,
            row_id=request.row_id,
            provider=self.provider,
            model_id=self.model_id,
            status="not_run",
            error_code=error_code,
        )

    def _invoke_transport(self, request: ModelRequest) -> tuple[str, float]:
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.transport, request)
        try:
            return future.result(timeout=request.timeout_seconds)
        except FutureTimeoutError as exc:
            future.cancel()
            raise TimeoutError("provider transport timed out") from exc
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    def _retry_delay(
        self,
        attempt: int,
        error: RetryableProviderError,
    ) -> float:
        requested = (
            error.retry_after_seconds
            if error.retry_after_seconds is not None
            else self.retry_base_seconds * (2**attempt)
        )
        bounded = min(max(requested, 0.0), self.max_backoff_seconds)
        remaining = max(self.max_backoff_seconds - bounded, 0.0)
        jitter = min(max(self.jitter_fn(min(bounded, 1.0)), 0.0), remaining)
        return bounded + jitter

    def generate(self, request: ModelRequest) -> ModelResponse:
        if request.provider != self.provider:
            raise ValueError("request provider does not match remote adapter")
        if not request.allow_remote or not self.allow_remote:
            return self._not_run(request, "remote_opt_in_required")
        if self.execution_policy is None:
            return self._not_run(request, "execution_policy_required")
        remote_policy = self.execution_policy.get("remote_providers")
        if not isinstance(remote_policy, Mapping) or remote_policy.get("allow_remote") is not True:
            return self._not_run(request, "execution_policy_remote_disabled")
        session_policy = self.execution_policy.get("current_session")
        if (
            not isinstance(session_policy, Mapping)
            or session_policy.get("provider_calls") != "enabled"
            or session_policy.get("network_access") != "enabled"
        ):
            return self._not_run(request, "execution_policy_session_disabled")
        policy_ceiling = remote_policy.get("cost_ceiling")
        if (
            isinstance(policy_ceiling, bool)
            or not isinstance(policy_ceiling, (int, float))
            or not isfinite(policy_ceiling)
            or policy_ceiling <= 0
            or request.cost_ceiling > policy_ceiling
        ):
            return self._not_run(request, "execution_policy_budget_required")
        if request.cost_ceiling <= 0 or self.cost_ceiling <= 0:
            return self._not_run(request, "cost_ceiling_required")
        if request.cost_ceiling > self.cost_ceiling:
            return self._not_run(request, "request_cost_ceiling_exceeds_adapter")
        if request.input_provenance != "independently_authored_synthetic":
            return self._not_run(request, "synthetic_input_required")

        started = perf_counter()
        attempts = 0
        while True:
            try:
                text, estimated_cost = self._invoke_transport(request)
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
                if (
                    isinstance(estimated_cost, bool)
                    or not isinstance(estimated_cost, (int, float))
                    or not isfinite(estimated_cost)
                ):
                    return ModelResponse(
                        request_hash=request.request_hash,
                        row_id=request.row_id,
                        provider=self.provider,
                        model_id=self.model_id,
                        status="provider_error",
                        error_code="invalid_cost_estimate",
                        latency_ms=(perf_counter() - started) * 1000,
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
            except RetryableProviderError as exc:
                if attempts >= request.max_retries:
                    return ModelResponse(
                        request_hash=request.request_hash,
                        row_id=request.row_id,
                        provider=self.provider,
                        model_id=self.model_id,
                        status="provider_error",
                        error_code=(
                            exc.error_code
                            if exc.error_code in PUBLIC_RETRY_ERROR_CODES
                            else "provider_error_redacted"
                        ),
                        latency_ms=(perf_counter() - started) * 1000,
                    )
                self.sleep_fn(self._retry_delay(attempts, exc))
                attempts += 1
            except TimeoutError:
                # A timed-out thread may still be active; retrying could duplicate a call.
                return ModelResponse(
                    request_hash=request.request_hash,
                    row_id=request.row_id,
                    provider=self.provider,
                    model_id=self.model_id,
                    status="timeout",
                    error_code="timeout",
                    latency_ms=(perf_counter() - started) * 1000,
                )
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
