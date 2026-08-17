from __future__ import annotations

import re

from .provenance import stable_hash

SECRET_PATTERNS = (
    re.compile(r"(?i)sk-[A-Za-z0-9_-]{12,}"),
    re.compile(r"(?i)gsk_[A-Za-z0-9_-]{12,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*[^\s,]+"),
)
IDENTIFIER_PATTERNS = (
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    re.compile(r"\b(?:PERSON|PATIENT|NHS)[-_][A-Z0-9]+\b", re.IGNORECASE),
)


def redact_text(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED_SECRET]", redacted)
    for pattern in IDENTIFIER_PATTERNS:
        redacted = pattern.sub("[REDACTED_IDENTIFIER]", redacted)
    return redacted


def redacted_hash(text: str) -> str:
    return stable_hash({"redacted_text": redact_text(text)})
