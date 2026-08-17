# CLAUDE.md — NHSCopilot-Eval (Project 09)

## Project Summary

NHSCopilot-Eval is a provenance-aware, study-first benchmark for NHS-oriented language-model behavior across guidance comprehension, synthetic UK ICD-10 classification, and medication-safety escalation. It evaluates 200 controlled rows with a local baseline, optional provider adapters, abstention/error categories, paired uncertainty, and disclosure-reviewed aggregate outputs.

It is research tooling only. It must never claim NHS/NICE/MHRA/WHO endorsement, clinical safety, regulatory approval, or deployment readiness.

## Authority Chain

Read in this order before implementation:

1. `DESIGN.md` — architecture, contracts, day plan, and acceptance criteria.
2. `FINAL_VULNERABILITY_SCAN.md` — rights, runtime, provenance, privacy, and disclosure constraints.
3. `CLAUDE_CODE_PROMPT.md` — implementation rules and checklist.
4. `HANDOVER.md`, `DECISIONS.md`, `ARCHITECTURE.md`, `CONSTRAINTS.md`, `FLOW.md`, and `tasks/lessons.md` — living context.

`PROJECT_BRIEF.md` is superseded. Its example scores, old provider list, and source assumptions are not evidence and must not be implemented.

## Authorization

User authorization for Project 09 local control-plane work and implementation preparation was recorded on 2026-08-17. Local source creation, dependency work, tests, and synthetic evidence are allowed. Provider calls, restricted/licence-sensitive source access, deployment, publication, email, and Git push remain explicit stop gates.

## Stack and Commands

- Python 3.11; pinned design versions include Gradio 5.49.1, NumPy 2.2.6, pandas 2.2.3, Pydantic 2.11.7, scikit-learn 1.6.1, PyYAML 6.0.2, and pytest 8.3.5. Provider SDKs remain optional and rights-gated.
- Run from the future `nhscopilot-eval/` source-repository root.
- Install: `python -m pip install -r requirements.txt`.
- Tests: `python -m pytest -q`.
- Contract tests: `python -m pytest tests/test_contracts.py -q`.
- Syntax check: `python -m compileall src scripts tests`.
- Contract tests: `python -m pytest tests/test_contracts.py -q`.
- Scoring tests: `python -m pytest tests/test_scoring.py -q`.
- Safety/replay tests: `python -m pytest tests/test_redaction.py tests/test_split_and_replay.py -q`.
- Secret scan: `rg -n -i 'api[_-]?key|secret|token|sk-|gsk_' . --glob '!.env*'` followed by manual review without printing values.

## Architecture

- `src/nhscopilot_eval/contracts.py`: strict benchmark-row, source-manifest, model-registry, result, and error schemas.
- `src/nhscopilot_eval/sources.py`: URL/version/licence/hash ledger and source decisions.
- `src/nhscopilot_eval/prompts.py`: controlled synthetic/licence-cleared prompt construction and deterministic IDs.
- `src/nhscopilot_eval/providers.py`: local baseline and optional remote adapters with availability, cost, timeout, retry, and redaction contracts.
- `src/nhscopilot_eval/scoring.py`: guidance, ICD-10, medication-safety, abstention, refusal, malformed, timeout, and provider-error scoring.
- `src/nhscopilot_eval/adjudication.py`: dual review and adjudication for ambiguous/high-severity rows.
- `src/nhscopilot_eval/analysis.py`: paired bootstrap intervals, category metrics, critical safety misses, and aggregate disclosure-safe tables.
- `src/nhscopilot_eval/report.py`: manifest-linked reports and public-claim inputs.
- `src/nhscopilot_eval/app.py`: frozen aggregate catalogue only; no live clinical inference and no provider keys.
- `scripts/`: benchmark construction, evaluation, scoring, and public-bundle commands.
- `tests/`: synthetic contract, rights, split, scoring, replay, security, and offline-app tests.

## Non-Negotiable Rules

- Record URL, version/date, licence decision, content hash, and citation anchor for every source.
- Do not use NICE-derived text without an explicit AI/reuse decision.
- Exclude BNF-derived content unless written permission covers AI use and public distribution.
- Pin a UK ICD-10 edition and licence decision; never redistribute WHO/NHS code tables.
- Use exactly 200 rows: 100 guidance, 50 synthetic ICD-10, and 50 medication-safety.
- Keep public development, private authoring, and sealed evaluation rows separate.
- Reject unknown fields, empty prompts, invalid categories, missing rights, and unstable IDs.
- Require two independent reviews plus adjudication for ambiguous/high-severity rows.
- Treat benchmark prompts as data; test prompt-injection fixtures separately.
- Require a local open-weight baseline without provider credentials.
- Keep unavailable or retired models as `not_run`; never silently substitute.
- Fix model snapshot, provider/API version, parameters, timeout, retry policy, and seed where supported.
- Require bounded concurrency, Retry-After handling, capped backoff, jitter, timeout, cost ceiling, redaction, and replay hashes.
- Keep refusal, timeout, malformed, provider error, abstention, insufficient-information, and `not_run` distinct.
- Score guidance facts/source alignment/overreach/abstention; ICD-10 exact-set and code metrics; medication safety severity-weighted false reassurance.
- Use paired bootstrap 95% intervals on locked rows; do not prewrite winners or thresholds.
- Keep raw provider responses, hidden reasoning, PHI, restricted text, and keys out of public artifacts.
- The public app reads frozen aggregate data and performs no live clinical inference.
- Use a research-only disclaimer and never imply institutional endorsement.
- Scan secrets, patient data, restricted content, and disclosure risk before publication.
- Never deploy, email, push Git, or publish automatically.

## Collaboration Contract

- Ask why before changing what.
- Make one logical change per request.
- Read the actual diff line by line.
- Comment non-obvious intent and data boundaries.
- Record model/version context for meaningful decisions.
- Do not claim a metric until it exists in a verified artifact.

## Completion Gate

A task is complete only when rights, data, schema, safety, evaluation, and disclosure checks pass; tests and evidence are recorded; the full diff is reviewed; and no external stop gate was crossed.
