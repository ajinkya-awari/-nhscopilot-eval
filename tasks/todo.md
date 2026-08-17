# tasks/todo.md — NHSCopilot-Eval

**Targets:** Faculty AI, NHS AI Lab, Accurx, Lumeon, Ada Health (research-evaluation relevance only)  
**Implementation window:** Days 43–45; local Project 09 authorization is active and external gates remain closed  
**Headline:** Versioned, risk-calibrated UK/NHS LLM evaluation—not a clinical leaderboard.

> **PROJECT 09 LOCAL AUTHORIZATION - 2026-08-17:** Local documentation, source preparation, tests, dependencies, and synthetic evidence are authorized. Rights-sensitive source access, provider calls, evaluation against remote models, deployment, publication, outreach, and Git push remain explicit stop gates.

## Pre-Implementation Gate

- [x] Project 09 local authorization recorded; external gates remain closed
- [x] Read FINAL_VULNERABILITY_SCAN.md, DESIGN.md, CLAUDE.md, CLAUDE_CODE_PROMPT.md, and lessons.md
- [x] Confirm no rights-sensitive source access, remote provider call, publication, or outreach has occurred; local source creation remains permitted

## Session Execution Policy — 2026-08-18

- [x] Keep this session Project 09-local, offline, and synthetic-only.
- [x] Do not run CPU tests, package installation, model downloads, provider calls, local training, or local model inference.
- [x] Reserve GPU-dependent model work for an explicit Kaggle or Google Colab notebook milestone.
- [x] Use only lightweight static checks for this session and record their evidence before advancing a gate.

## Independent Local Guardrails — 2026-08-18

- [x] Add a synthetic-only rights ledger with blocked external-source entries.
- [x] Add an explicit model registry with pending availability and `not_run` semantics.
- [x] Update FLOW.md and DECISIONS.md without changing rights or provider gates.
- [x] Run the lightweight PowerShell policy guardrail; do not run Python or CPU tests.
- [x] Record guardrail output in HANDOVER.md and evidence; keep Kaggle/Colab pytest pending.

## Day 43 — Rights, Contracts, and Benchmark Authoring

**Gate:** Do not run providers or create a public bundle until every row has a rights decision and
the hidden split is frozen.

### 43.1 Source and licence ledger

- [ ] Record current NICE candidate IDs NG28, NG136, NG12, NG253, and CG187 only after live verification
- [ ] Record URL, revision date, document hash, section anchor, licence, geography, and AI-permission status
- [ ] Exclude BNF unless written permission covers AI use and public distribution; otherwise select MHRA/public sources
- [ ] Freeze a UK ICD-10 edition/licence decision; do not copy code tables into public data
- [x] Write and record the fully synthetic fallback decision; local generated rows remain unreleased until review

### 43.2 Contracts and schemas

- [x] Write contract tests for BenchmarkRow, ModelRequest, ModelResponse, SourceManifest, and PublicBundle; local execution is intentionally deferred
- [ ] Run the CPU-bound contract tests only in Kaggle or Google Colab; do not run them locally
- [x] Implement strict Pydantic contracts and deterministic canonical JSON/hash functions locally
- [x] Add synthetic fixtures for PHI-like text, prompt injection, restricted-source markers, and malformed rows
- [ ] Record the Kaggle/Colab contract-test output in the day review before advancing this gate

### 43.3 Authoring and review

- [x] Generate exactly 100 guidance, 50 synthetic ICD-10, and 50 medication-safety rows locally
- [x] Use safe/unsafe/review/insufficient-information medication labels and severity classes
- [x] Attach source/version/anchor/rubric metadata to every generated row
- [ ] Perform two independent reviews for ambiguous/high-severity rows and record adjudications
- [ ] Freeze public development metadata and private locked prompts/labels with hashes

**Day 43 smoke test:** schema validation, rights ledger, row counts, split disjointness, PHI scan,
and review agreement all pass; otherwise use the synthetic/licence-cleared fallback.

**Commit message for future implementation:** docs/data: freeze rights ledger and benchmark contracts — Day 43

### 43.0 First Projectlocal milestone — provenance and execution scaffold

- [x] Create the separate `nhscopilot-eval/` source boundary; do not add source rows to the planning folder.
- [x] Record a synthetic-authorship fallback manifest with no external source content admitted.
- [x] Add benchmark target/split configuration without authoring rows or labels.
- [x] Add an offline execution policy with remote providers disabled and GPU notebook work deferred.
- [x] Run lightweight static boundary and forbidden-content checks only; do not run CPU tests.
- [x] Update `HANDOVER.md` with exact command output and remaining rights/data gates.

## Day 44 — Providers, Scoring, Replay, and Analysis

**Gate:** Day 43 evidence is complete; no provider call may proceed with missing rights, missing
model metadata, missing budget, or a non-sealed evaluation split.

### 44.1 Provider adapters

- [x] Write adapter tests using local fixtures; no credentials required
- [x] Implement local fixture adapter and exact model-registry policy validation
- [x] Implement an SDK-neutral optional remote adapter behind explicit allow-remote and cost ceiling; provider SDK calls remain disabled
- [x] Add not_run semantics, request hashes, parameter capture, and redacted logging boundaries
- [ ] Test Retry-After, capped backoff, bounded jitter, timeout, rate limit, malformed response, and provider error

### 44.2 Category scorers

- [x] Implement guidance atomic-fact, citation, harmful-addition, completeness, and abstention scorer
- [x] Implement ICD-10 normalization, exact-set, primary-code, micro/macro F1, and syntax-invalid diagnostics without redistributing code tables
- [x] Implement medication tri/quad-state and unsafe-false-reassurance scorer
- [x] Raise loudly for unknown category instead of silently skipping medication safety
- [x] Add synthetic fixtures for refusal, overconfident unsafe advice, fabricated citations, and partial-answer extensions

### 44.3 Analysis

- [x] Implement paired bootstrap 95% intervals over paired rows
- [x] Produce category aggregation hooks and preserve status/availability fields
- [x] Keep no-winner policy in analysis and reporting code
- [x] Write replay records with model, prompt, config, source, and response hashes

**Day 44 smoke test:** local baseline evaluates fixtures end-to-end with zero secrets and all three
scorers; optional providers are skipped cleanly when unavailable.

**Commit message for future implementation:** feat(eval): add provider contracts and risk-aware scoring — Day 44

## Day 45 — Disclosure Review and Aggregate Leaderboard

**Gate:** Day 44 tests and manifests pass; publication remains blocked if any rights/privacy/safety
or secret scan fails.

### 45.1 Public bundle

- [x] Implement export of only permitted synthetic/licence-cleared development projections and aggregate results
- [ ] Keep hidden test prompts/labels, raw provider outputs, source passages, and adjudication ledger private
- [x] Generate bundle code, dataset card, limitations, attribution, research-only disclaimer, and model availability policy
- [x] Scan the generated public projection for secrets, PHI, restricted text, answer-key leakage, and unsupported claims

### 45.2 Leaderboard

- [x] Build aggregate-only Gradio/static app with no provider keys, uploads, or live clinical inference
- [x] Display category scores, uncertainty, failures, abstentions, not_run rows, versions, and rights-cleared source links when available
- [x] Add visible “not clinical advice” and “does not establish safety/regulatory compliance” notices
- [ ] Run network-disabled smoke test in Kaggle/Colab or approved environment; local Python execution remains disabled

### 45.3 Final review

- [ ] Verify all public claims against manifest rows and remove any directional winner language
- [ ] Record licence, privacy, clinical-safety, reproducibility, and cross-project review sign-offs
- [ ] Keep publication and outreach as user-reviewed drafts until portfolio release and explicit authorization

**Day 45 smoke test:** disclosure scan reports zero secrets/PHI/restricted text/raw outputs; aggregate
app works offline; all final manifests and hashes are reproducible.

**Commit message for future implementation:** docs: add disclosure-reviewed aggregate leaderboard — Day 45

## Final Verification Checklist

- [ ] All DESIGN.md §8 acceptance criteria pass with fresh evidence
- [ ] All three checklist copies are byte-for-byte identical
- [ ] CLAUDE.md and prompt contain exactly 23 rules in order
- [ ] Scan covers 10 areas and lessons map every NEEDS FIX
- [x] All active files repeat local authorization and external stop gates
- [ ] No non-Markdown implementation files exist in the planning folder
- [ ] No cross-project implementation or vocabulary contamination exists
- [ ] PORTFOLIO_STATUS.md is updated only after every gate above passes
