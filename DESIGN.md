# DESIGN.md — NHSCopilot-Eval (Project 09)

**Implementation window:** Days 43–45; local Project 09 implementation is authorized and no source repository exists yet.

> **PROJECT 09 LOCAL AUTHORIZATION - 2026-08-17:** Local documentation, source preparation, tests, dependencies, and synthetic evidence are authorized. Rights-sensitive source access, provider calls, evaluation against remote models, deployment, publication, outreach, and Git push remain explicit stop gates.

> **External-action gate:** local source creation, tests, dependencies, and synthetic evaluation
> are authorized. Do not access rights-sensitive sources, call paid/remote model APIs, publish a
> dataset or Space, or send outreach without separate approval.

> **FINAL_VULNERABILITY_SCAN.md overrides this file where they conflict.**

## §0. Design Decisions

### Divergent exploration

| Option | Scope | Strength | Failure mode |
|---|---|---|---|
| A. Brief-faithful remote leaderboard | Four named remote models, 200 items, one score | Fast and recognizable | Paid APIs, retired model IDs, no reproducible replay, copyright/privacy exposure |
| B. Local-only benchmark | Open-weight local models and synthetic fixtures | Reproducible and zero-cost | Less direct comparison with commercial systems |
| C. Evidence-first hybrid (selected) | Frozen licensed/derived benchmark, deterministic local baseline, optional provider adapters | Strong NHS evaluation story with auditable provenance and graceful unavailable rows | More adapter and disclosure work |

### Convergent decisions

1. **Study-first, not product-first:** measure factuality, coding exactness, medication-safety
   severity, citation faithfulness, abstention, and latency; this is not clinical decision support.
2. **Content boundary:** use short, independently authored or licence-cleared prompts. NICE
   content requires licence/AI permission review; BNF is excluded. Medication items use public
   MHRA Drug Safety Updates and other explicitly licensed public sources. ICD-10 uses a
   licence-reviewed code subset and synthetic vignettes; do not redistribute WHO/NHS code tables.
   If the intended topics remain diabetes, hypertension, suspected cancer, sepsis, and acute
   heart failure, the implementation-time candidate set is NG28, NG136, NG12, NG253, and CG187.
   The obsolete brief identifiers CG127, NG17, NG185, and CG191 must not be used without a fresh
   NICE verification and replacement decision.
3. **Model matrix:** a deterministic local open-weight baseline is mandatory. OpenAI, Anthropic,
   and Hugging Face adapters are optional and run only with user-provided credentials and a
   recorded model snapshot, terms, region, timestamp, and cost. An unavailable model is reported
   as not_run, never silently replaced.
4. **Evaluation contract:** every row has a rubric, source/version, answer key, severity class,
   citation requirement, and adjudication status. Two independent rubric passes plus adjudication
   are required for ambiguous or safety-critical items.

## §1. Project Goal

Build a reproducible evaluation harness for NHS-oriented language-model behavior on 200 synthetic
and licence-cleared tasks across NICE-style guidance comprehension, synthetic ICD-10 coding, and
medicines-safety communication. Publish only a disclosure-reviewed dataset card, aggregate results,
and a static/Space leaderboard that clearly says “research evaluation, not clinical advice.”

**Headline policy:** report measured category-level results with uncertainty and model availability;
do not prewrite a winner, accuracy value, clinical efficacy claim, or NHS endorsement.

**Target relevance:** Faculty AI, NHS AI Lab, Accurx, Lumeon, Ada Health, and related teams get an
auditable evaluation template, failure taxonomy, and reproducible local replay—not a sales claim.

## §2. Zero-Cost Stack and Reproducibility

### 2.1 Runtime pins

    python==3.12.10
    datasets==3.6.0
    gradio==5.49.1
    numpy==2.2.6
    pandas==2.2.3
    pydantic==2.11.7
    httpx==0.28.1
    scikit-learn==1.6.1
    pyyaml==6.0.2
    pytest==8.3.5
    ruff==0.11.8

Provider SDKs are optional extras and never required for the local smoke test:
openai 1.82.0, anthropic 0.52.0, and huggingface_hub 0.31.4. The implementation must verify
availability and hashes at runtime; package installation and source access remain subject to the
local implementation authorization and the separate rights/provider gates.

### 2.2 Model registry

configs/models.yaml stores provider, exact model ID/snapshot, tokenizer revision, context limit,
temperature, seed support, endpoint region, terms URL, cost estimate, and status. The registry
must contain a local open-weight baseline and may contain gpt-4o, an available Anthropic snapshot,
and an available Hugging Face model only after live availability verification.

### 2.3 Data and licence boundary

No raw NICE PDFs, BNF text, WHO/NHS ICD-10 tables, patient records, API keys, prompts containing
personal data, provider responses, or hidden model traces enter a public artifact. Store a source
URL, version/date, licence decision, checksum, excerpt hash, and author/adjudicator IDs in the
private manifest. Public rows contain only independently authored text, short permitted references,
labels, and disclosure-reviewed aggregates.

## §3. Architecture

    nhscopilot-eval/
    ├── pyproject.toml
    ├── requirements.txt
    ├── configs/
    │   ├── benchmark.yaml
    │   └── models.yaml
    ├── src/nhscopilot_eval/
    │   ├── contracts.py
    │   ├── sources.py
    │   ├── prompts.py
    │   ├── providers.py
    │   ├── scoring.py
    │   ├── adjudication.py
    │   ├── analysis.py
    │   ├── report.py
    │   └── app.py
    ├── scripts/
    │   ├── build_benchmark.py
    │   ├── run_eval.py
    │   ├── score_eval.py
    │   └── build_public_bundle.py
    ├── tests/
    │   ├── test_contracts.py
    │   ├── test_scoring.py
    │   ├── test_redaction.py
    │   ├── test_split_and_replay.py
    │   └── fixtures/
    ├── data/
    │   ├── public/
    │   └── private/
    └── artifacts/public_bundle/

## §4. Component Designs

### §4.1 Contracts and benchmark rows

BenchmarkRow uses row_id, category, prompt, answer_key, rubric_version, source_id, source_version,
licence_status, severity, requires_abstention, and split. Pydantic rejects unknown fields, empty
prompts, unapproved categories, missing source decisions, and public rows carrying restricted text.
IDs and hashes are deterministic.

### §4.2 Dataset construction and split

Create 200 rows only after licence decisions: 100 guidance-comprehension, 50 synthetic ICD-10
vignettes, and 50 medication-safety scenarios. Keep a private authoring set and a locked evaluation
set; do not tune prompts or rubrics on evaluation outputs. Record class/severity balance and source
versions.

### §4.3 Provider adapters and safety

All adapters implement a common generate(ModelRequest) -> ModelResponse interface. Requests contain
synthetic text only, timeout, retry budget, and a stable request hash. Responses are redacted before
storage; raw model text and hidden reasoning are never logged publicly. Retry only transient statuses
with Retry-After, capped exponential backoff, bounded jitter, and injectable sleep. Remote adapters
require an explicit allow-remote flag and a cost ceiling.

### §4.4 Scoring and adjudication

Guidance uses rubric dimensions for factual support, completeness, citation/source alignment,
harmful overreach, and abstention. ICD-10 reports exact-set accuracy, micro/macro precision/recall/F1,
hierarchy-aware secondary diagnostics, and unsupported-code rate. Medication safety reports a
severity-weighted confusion matrix, unsafe false-negative rate as primary safety metric,
rationale/source alignment, and abstention quality. All categories report paired bootstrap 95% CIs,
missing/not-run counts, latency, token/cost estimate, and deterministic replay hashes. Ambiguous rows
require two raters and documented adjudication.

### §4.5 Analysis and claims

Use paired bootstrap intervals over identical rows and category macro-averages; no winner gate.
Report availability, failures, abstentions, cost, and version drift. Results are descriptive, not
evidence of clinical safety or deployment readiness. Any public claim maps to a manifest row and
disclosure review.

### §4.6 Leaderboard app

The default app reads a frozen aggregate JSON/CSV bundle. It has no provider keys, no live clinical
inference, no user-text upload, a visible not-clinical-advice banner, source/licence links, model
availability labels, and a reproducibility link. A Space is optional; a static catalogue is the
required fallback.

## §5. Day-by-Day Execution

| Day | Goal | Blocking gate | Integrity-preserving fallback |
|---|---|---|---|
| 43 | Contracts, licence ledger, authoring, rubric QA | 200 rows pass schema/licence checks; source manifest and dual-rater sample agree; no restricted text in public candidate bundle | Reduce public bundle to synthetic/licence-cleared rows and document excluded sources |
| 44 | Provider adapters, replay, scoring, analysis | Local baseline runs on locked set; optional remote rows have versions/cost and no key leakage; scoring tests and bootstrap analysis pass | Mark unavailable providers not_run; publish local baseline only |
| 45 | Disclosure review, aggregate bundle, leaderboard | Public bundle scan passes; app uses frozen aggregates only; README states limitations and no clinical claim | Publish static catalogue and local reproduction instructions; do not create a live Space |

## §6. Output Artifacts

| File | Purpose |
|---|---|
| data/public/benchmark.jsonl | Synthetic/licence-cleared public rows |
| artifacts/public_bundle/results.csv | Aggregate scores, CIs, availability, and failure counts |
| artifacts/public_bundle/manifest.json | Hashes, versions, licences, and run metadata |
| artifacts/public_bundle/dataset_card.md | Scope, provenance, limitations, and non-clinical disclaimer |
| artifacts/public_bundle/leaderboard.html | Static fallback rendering |
| reports/adjudication.csv | Restricted disagreement ledger, never public |

## §7. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---:|---:|---|
| NICE AI/copyright permission incomplete | High | Critical | Licence ledger; independently authored prompts; permission/status before use |
| BNF content reused | High | Critical | Exclude BNF; use public MHRA/SPS sources after licence review |
| WHO/NHS ICD-10 redistribution breach | Medium | Critical | Licence-reviewed subset; no code-table redistribution |
| Provider model retires or changes | High | High | Exact registry, availability gate, not_run semantics |
| API key/clinical text leakage | Medium | Critical | Synthetic-only inputs, redaction tests, no raw logs |
| Prompt injection in benchmark text | Medium | High | Treat rows as data; fixed system prompt; injection fixtures |
| Medication unsafe false negative | Medium | Critical | Severity weighting, abstention, dual adjudication |
| Guideline version drift | High | High | Version/date/hash manifest and locked set |
| Small benchmark overclaims ranking | High | High | CIs, paired rows, category macro scores, no winner claim |
| Remote quota/cost failure | High | Medium | Local baseline, cost ceiling, retry/backoff, not_run status |
| Public Space executes live inference | Medium | High | Aggregate-only app, no secrets, network-disabled smoke test |
| Human annotation disagreement | Medium | High | Two passes, adjudication, disagreement report |

## §8. Acceptance Criteria

### Governance and provenance
- [x] Project 09 local authorization is recorded; external rights/provider/publication gates remain active
- [x] No rights-sensitive source access, remote provider call, publication, or outreach has occurred; local source creation remains permitted
- [ ] PROJECT_BRIEF.md is marked superseded and not an implementation authority
- [ ] Every public row has deterministic row_id, source decision, version, and content hash
- [ ] Private manifests and restricted artifacts are gitignored and never uploaded

### Dataset and licensing
- [ ] Exactly 200 rows exist: 100 guidance, 50 ICD-10, 50 medication-safety
- [ ] Every row passes strict Pydantic validation with unknown fields rejected
- [ ] NICE AI/reuse decision is recorded before any NICE-derived content is used
- [ ] Guideline IDs, revision dates, canonical URLs, and document hashes are verified; obsolete identifiers are rejected
- [ ] No BNF text or derivative content is present
- [ ] ICD-10 source/licence decision is recorded; no WHO/NHS code table is redistributed
- [ ] Public rows contain only synthetic or licence-cleared text
- [ ] Category, severity, abstention, and split distributions are reported
- [ ] Locked evaluation rows are not used for prompt/rubric tuning

### Providers and runtime
- [ ] Local open-weight baseline runs without provider credentials
- [ ] Optional provider adapters use exact registry IDs/snapshots and availability checks
- [ ] Unavailable or retired models are not_run, never silently substituted
- [ ] Remote execution requires explicit opt-in and a recorded cost ceiling
- [ ] Inputs are synthetic-only and raw responses/hidden reasoning are not public
- [ ] Retry honors Retry-After, capped backoff, bounded jitter, and injectable timing
- [ ] Timeouts, rate limits, failures, and latency are recorded
- [ ] .env is ignored and repository history contains no keys

### Scoring and analysis
- [ ] Guidance rubric scores factual support, completeness, source alignment, overreach, and abstention
- [ ] ICD-10 exact-set, micro/macro F1, and unsupported-code rate are reported
- [ ] Medication safety reports severity-weighted confusion and unsafe false-negative rate
- [ ] Ambiguous/high-severity rows receive two independent ratings and adjudication
- [ ] Bootstrap 95% CIs are computed on paired locked rows
- [ ] Missing, not_run, abstention, and provider-error counts are separate
- [ ] No metric or winner is prewritten before evaluation
- [ ] Replay hashes reproduce prompts, configs, and outputs without exposing secrets

### Public bundle and safety
- [ ] Public bundle contains aggregates, manifest, dataset card, and no restricted text
- [ ] Leaderboard reads frozen aggregates and performs no live clinical inference
- [ ] App displays not-clinical-advice and model availability/version labels
- [ ] Network-disabled app smoke test passes
- [ ] Public claims map to recorded rows and disclose uncertainty, limitations, and licences
- [ ] No NHS, NICE, MHRA, WHO, or company endorsement is implied
- [ ] Static catalogue fallback is documented if a zero-cost Space is unavailable
- [ ] Final disclosure scan reports zero secrets, patient data, raw provider outputs, or prohibited content
