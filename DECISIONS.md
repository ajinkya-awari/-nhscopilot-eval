# DECISIONS — NHSCopilot-Eval

Current state and next action: [`STATUS.md`](STATUS.md). This file records rationale and historical
decisions; it is not a substitute for fresh evidence.

## D-001: Codex and Claude bootstrap files

Use root `AGENTS.md` for Codex discovery and `CLAUDE.md` for Claude Code. Both reference the same authority chain and living records.

## D-002: Evidence-first hybrid benchmark

Keep the selected evidence-first hybrid design: local baseline first, optional provider adapters, synthetic/licence-cleared rows, hidden evaluation labels, and aggregate-only public outputs.

## D-003: Superseded brief is not evidence

`PROJECT_BRIEF.md` remains historical context. Its example scores, old model names, and source assumptions cannot enter code, reports, or claims.

## D-004: Local-first authorization

Local documentation, source preparation, tests, dependencies, and synthetic fixtures are allowed. Rights-sensitive access, provider calls, publication, and deployment remain gated.

## D-005: CPU verification boundary

Contract tests are authored in the local source boundary, but CPU-bound pytest execution is deferred
to Kaggle or Google Colab by explicit user instruction. Local verification uses PowerShell static
checks only; no test result is inferred from source inspection.

## D-006: Independent rights/model guardrails

Keep a synthetic-only rights ledger and a model registry with exact-snapshot and availability gates
before row authoring or provider execution. Unverified models remain pending or `not_run`; Project
09 does not train models. A later GPU notebook may evaluate an explicitly selected model, subject to
synthetic-input, rights, cost, and disclosure gates.

## D-007: Lightweight local generation boundary

The deterministic synthetic generator may run locally because it is small, offline, and does not
download packages, models, or source content. Its private/sealed JSONL outputs remain ignored and
unreleased. CPU-bound pytest, model inference, training, provider calls, and network smoke tests
remain delegated to Kaggle/Colab or an explicitly approved environment.

## D-008: Repository publication versus benchmark release

The user explicitly authorized pushing the source repository to GitHub; `3aa486e` is the current
remote tip. This does not authorize benchmark publication, provider execution, deployment, outreach,
rights-sensitive access, clinical claims, or regulatory claims.
