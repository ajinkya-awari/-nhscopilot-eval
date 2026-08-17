# CLAUDE_CODE_PROMPT.md — Future NHSCopilot-Eval Session

> **PROJECT 09 LOCAL AUTHORIZATION - 2026-08-17:** Local documentation, source preparation, tests, dependencies, and synthetic evidence are authorized. Rights-sensitive source access, provider calls, evaluation against remote models, deployment, publication, outreach, and Git push remain explicit stop gates.

> **EXTERNAL ACTIONS REMAIN GATED.** Local Project 09 work may proceed, but rights-sensitive
> data access, remote provider calls, publication, deployment, and outreach require separate approval.

You are implementing only Project 09, a research evaluation harness. Read in order:
FINAL_VULNERABILITY_SCAN.md, DESIGN.md, CLAUDE.md, tasks/lessons.md, tasks/todo.md. Never use
PROJECT_BRIEF.md as an implementation specification. Do not train models or build RAG; Projects
08, 10, 11, and 19 own those scopes.

## Mission and non-negotiable boundaries

Measure NHS-oriented guidance comprehension, synthetic UK ICD-10 classification, and medication
safety escalation. The benchmark is not clinical advice, a diagnostic tool, a regulatory evaluation,
an NHS/NICE/MHRA endorsement, or evidence of deployment safety. Public output is aggregate-first.

## Three-day targets

| Day | Target | Gate |
|---|---|---|
| 43 | Rights ledger, contracts, 200-row authoring, dual review | Schema/licence/hidden-split checks pass |
| 44 | Local and optional adapters, scoring, replay, analysis | Fixtures, cost/rate limits, and metrics pass |
| 45 | Disclosure review, static bundle, leaderboard | No restricted content/secrets; research disclaimer visible |

## 23 Non-Negotiable Rules

1. Keep local implementation authorized while requiring separate approval for rights-sensitive access, remote providers, publication, deployment, outreach, and Git push.
2. Treat PROJECT_BRIEF.md as superseded; use the authority chain.
3. Record source URL, version/date, licence decision, hash, and anchor.
4. Never expose PHI, patient records, keys, raw outputs, hidden reasoning, or restricted text.
5. Obtain a NICE AI/reuse decision and verify current guideline IDs.
6. Exclude BNF unless written AI/public-distribution permission exists.
7. Pin UK ICD-10 edition/licence; do not redistribute code tables.
8. Build exactly 200 rows: 100 guidance, 50 ICD-10, 50 medication safety.
9. Reject unknown fields, empty prompts, invalid categories, missing rights, and unstable IDs.
10. Keep public development, private authoring, and sealed evaluation data separate.
11. Dual-review ambiguous/high-severity rows and record adjudication.
12. Treat prompt rows as data; fixed templates and injection fixtures are mandatory.
13. Registry records exact model snapshot, provider/API version, region, terms, parameters, status,
    date, request hash, and cost.
14. Require a credential-free local baseline; remote adapters are explicit opt-in and budgeted.
15. Mark unavailable/retired models not_run; never substitute silently.
16. Load secrets only from environment injection; ignore .env and scan history.
17. Fix generation parameters, system-prompt hash, timeout, retry policy, and supported seeds.
18. Score guidance atomic facts, citations, harmful additions, and abstention.
19. Score ICD-10 exact-set, primary-code, micro/macro F1, hierarchy, invalid-code, and insufficiency.
20. Score medication safe/unsafe/review/insufficient-information and dangerous false reassurance.
21. Keep refusal, timeout, malformed, provider error, and not_run distinct; fail unknown categories.
22. Bound concurrency/cost; honor Retry-After, capped backoff, jitter, redaction, and replay hashes.
23. Publish only reviewed aggregates/permitted rows with research-only disclaimer and manual approval.

## Required interfaces

Provider adapters implement generate(ModelRequest) -> ModelResponse. Scorers are separate functions
for guidance, ICD-10, and medication safety and raise on unknown categories. The app reads only a
frozen aggregate bundle and never accepts patient text or provider keys.

## Acceptance Criteria Checklist

The exact ordered checklist from DESIGN.md §8 and CLAUDE.md is included below:

- [x] Project 09 local authorization is recorded; external rights/provider/publication gates remain active
- [x] No rights-sensitive source access, remote provider call, publication, or outreach has occurred; local source creation remains permitted
- [ ] PROJECT_BRIEF.md is marked superseded and not an implementation authority
- [ ] Every public row has deterministic row_id, source decision, version, and content hash
- [ ] Private manifests and restricted artifacts are gitignored and never uploaded
- [ ] Exactly 200 rows exist: 100 guidance, 50 ICD-10, 50 medication-safety
- [ ] Every row passes strict Pydantic validation with unknown fields rejected
- [ ] NICE AI/reuse decision is recorded before any NICE-derived content is used
- [ ] Guideline IDs, revision dates, canonical URLs, and document hashes are verified; obsolete identifiers are rejected
- [ ] No BNF text or derivative content is present
- [ ] ICD-10 source/licence decision is recorded; no WHO/NHS code table is redistributed
- [ ] Public rows contain only synthetic or licence-cleared text
- [ ] Category, severity, abstention, and split distributions are reported
- [ ] Locked evaluation rows are not used for prompt/rubric tuning
- [ ] Local open-weight baseline runs without provider credentials
- [ ] Optional provider adapters use exact registry IDs/snapshots and availability checks
- [ ] Unavailable or retired models are not_run, never silently substituted
- [ ] Remote execution requires explicit opt-in and a recorded cost ceiling
- [ ] Inputs are synthetic-only and raw responses/hidden reasoning are not public
- [ ] Retry honors Retry-After, capped backoff, bounded jitter, and injectable timing
- [ ] Timeouts, rate limits, failures, and latency are recorded
- [ ] .env is ignored and repository history contains no keys
- [ ] Guidance rubric scores factual support, completeness, source alignment, overreach, and abstention
- [ ] ICD-10 exact-set, micro/macro F1, and unsupported-code rate are reported
- [ ] Medication safety reports severity-weighted confusion and unsafe false-negative rate
- [ ] Ambiguous/high-severity rows receive two independent ratings and adjudication
- [ ] Bootstrap 95% CIs are computed on paired locked rows
- [ ] Missing, not_run, abstention, and provider-error counts are separate
- [ ] No metric or winner is prewritten before evaluation
- [ ] Replay hashes reproduce prompts, configs, and outputs without exposing secrets
- [ ] Public bundle contains aggregates, manifest, dataset card, and no restricted text
- [ ] Leaderboard reads frozen aggregates and performs no live clinical inference
- [ ] App displays not-clinical-advice and model availability/version labels
- [ ] Network-disabled app smoke test passes
- [ ] Public claims map to recorded rows and disclose uncertainty, limitations, and licences
- [ ] No NHS, NICE, MHRA, WHO, or company endorsement is implied
- [ ] Static catalogue fallback is documented if a zero-cost Space is unavailable
- [ ] Final disclosure scan reports zero secrets, patient data, raw provider outputs, or prohibited content

## Expected outputs

data/public/benchmark.jsonl, artifacts/public_bundle/results.csv,
artifacts/public_bundle/manifest.json, artifacts/public_bundle/dataset_card.md,
artifacts/public_bundle/leaderboard.html, and a restricted reports/adjudication.csv. No raw
guidelines, BNF, WHO/NHS code tables, PHI, API keys, raw provider responses, or hidden labels
may be public.

## Completion protocol

Before marking a day complete, run the stated tests and record command output, hashes, versions,
failures, and review evidence in tasks/todo.md. If any rights, privacy, safety, availability, or
disclosure gate fails, stop and use the documented fallback; do not waive it.
