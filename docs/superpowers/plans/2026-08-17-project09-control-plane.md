# Project 09 Control Plane and Local Implementation Plan

> **For agentic workers:** Use this plan task-by-task. Keep the documentation/control-plane changes isolated to Project 09 and run the structural checks after each batch.

**Goal:** Install the Project 09 control plane, then build the local synthetic-only evaluation foundation while keeping rights-sensitive data, remote providers, and heavy execution outside this workspace.

**Architecture:** Root instructions bootstrap agents; `.claude/` defines specialists, commands, hooks, rules, skills, and permissions; field-guide documents preserve continuity and evidence. The separate `nhscopilot-eval/` source boundary begins with provenance and execution-policy configuration, followed by strict contracts, local fixtures, and aggregate-only evaluation. GPU-dependent model work is exported to a user-run Kaggle or Google Colab notebook and is never executed locally.

**Tech Stack:** Markdown, YAML frontmatter, JSON settings, POSIX shell hooks, Python project commands.

## Global Constraints

- Use only Project 09 terminology and contracts.
- Treat `PROJECT_BRIEF.md` as superseded; never use its example metrics as results.
- Keep BNF, WHO/NHS code tables, PHI, patient records, raw provider responses, keys, and hidden labels out of public artifacts.
- Do not call providers, fetch rights-sensitive sources, deploy, publish, email, or push Git. Keep the source repository strictly inside the separate local nhscopilot-eval/ boundary.
- Do not auto-commit.

## Execution Policy for This Session

- Local work is offline and synthetic-only.
- Do not run `pytest`, `compileall`, package installation, model downloads, provider calls, or local model training/inference.
- Applicable verification is limited to lightweight PowerShell file, JSON/YAML-text, boundary, and forbidden-content checks.
- Any GPU-dependent baseline or training workflow must be a later notebook artifact for Kaggle or Google Colab, with explicit user opt-in, synthetic inputs, and no restricted-source access.
- The first implementation milestone must not author benchmark rows or claim metrics.

## Current Implementation Slice

The control-plane documents already exist. The first verified local milestone is the source-boundary scaffold and synthetic fallback decision: a separate source directory, package metadata, private/public/sealed directory intent, a source manifest with no external content admitted, and an execution policy that makes remote/GPU work an explicit later step. Contracts and row authoring follow only after this milestone is structurally verified.

### Task 1: Bootstrap and authority records

- [x] Create `AGENTS.md` and tailored `CLAUDE.md`.
- [ ] Create the design record and collaboration index.
- [ ] Confirm the authority chain and authorization boundaries.

### Task 2: NHS evaluation control plane

- [ ] Create six project-specific agents.
- [ ] Create three provenance/evaluation/security commands or commands adapted to this project.
- [ ] Create safe hooks, path-aware rules, workflow skill, and settings.

### Task 3: Project 09 prompt pack

- [ ] Create all 15 prompts with NHS evaluation-specific inputs, outputs, tests, licensing, and stop gates.
- [ ] Scan every prompt for contamination from unrelated projects.

### Task 4: Field-guide records

- [ ] Create handover, decisions, architecture, constraints, flow, test, rollback, feature, and bug records.
- [ ] Add the first authorization and superseded-brief decisions.

### Task 5: Existing-plan consistency

- [ ] Replace contradictory portfolio-freeze banners with dated local authorization plus external stop gates.
- [ ] Preserve historical freeze context in `DECISIONS.md`.

### Task 6: Verification

- [ ] Enumerate expected files and check non-empty content.
- [ ] Parse JSON and validate frontmatter.
- [ ] Search for unrelated project terms, fabricated example scores, stale freeze text, and secrets.
- [ ] Read the full scoped diff and update `HANDOVER.md`.

### Task 7: Milestone 1 — Projectlocal provenance and execution scaffold

**Files:**
- Create: `nhscopilot-eval/README.md`
- Create: `nhscopilot-eval/pyproject.toml`
- Create: `nhscopilot-eval/.gitignore`
- Create: `nhscopilot-eval/configs/benchmark.yaml`
- Create: `nhscopilot-eval/configs/source_manifest.yaml`
- Create: `nhscopilot-eval/configs/execution.yaml`
- Create: `nhscopilot-eval/docs/evidence/milestone-1-static-check-2026-08-18.md`
- Create: `nhscopilot-eval/data/public/.gitkeep`
- Create: `nhscopilot-eval/data/private/.gitkeep`
- Create: `nhscopilot-eval/data/sealed/.gitkeep`

**Interfaces:**
- `configs/source_manifest.yaml` records only the synthetic-authorship fallback until a future rights decision admits an external source.
- `configs/benchmark.yaml` reserves the 100/50/50 category target and disjoint public/private/sealed split without creating rows.
- `configs/execution.yaml` is the single execution policy: offline local checks only by default; GPU notebook execution is opt-in and remote providers remain disabled.

- [x] Write the source-boundary configuration first; do not add benchmark content, provider keys, model files, or generated artifacts.
- [x] Verify with lightweight static checks that every expected file exists, the three data boundaries are present, remote execution is disabled, and no restricted markers or fabricated metrics occur in the new source boundary.
- [x] Record evidence in `HANDOVER.md`; leave contracts, row authoring, provider adapters, scoring, and notebook execution for later milestones.

### Task 8: Milestone 2 — Strict contracts and synthetic fixtures

**Files:**
- Create: `nhscopilot-eval/src/nhscopilot_eval/contracts.py`
- Create: `nhscopilot-eval/src/nhscopilot_eval/provenance.py`
- Create: `nhscopilot-eval/tests/test_contracts.py`
- Create: `nhscopilot-eval/tests/fixtures/`
- Create: `nhscopilot-eval/tests/fixtures/contract_cases.yaml`
- Create: `nhscopilot-eval/docs/KAGGLE_COLAB_TEST_RUN.md`
- Create: `nhscopilot-eval/docs/evidence/milestone-2-static-check-2026-08-18.md`

Implement strict Pydantic contracts and deterministic canonical hashes only after Milestone 1. Follow test-first development by authoring tests before production contracts. Do not run the CPU-bound pytest suite locally; the reproducible command and expected scope are documented for a later Kaggle or Google Colab run. Local verification is limited to source-file and policy scans.

Required interfaces:

- `canonical_json(value: object) -> str` produces sorted, compact, UTF-8-safe JSON.
- `stable_hash(value: object) -> str` returns a sha256-prefixed digest.
- `make_row_id(category: str, prompt: str, source_id: str, split: str) -> str` returns a deterministic row ID.
- `BenchmarkRow`, `SourceManifest`, `ModelRequest`, `ModelResponse`, and `PublicBundle` reject unknown fields and invalid safety/provenance states.
- `ModelRequest.request_hash` and `ModelResponse.response_hash` are deterministic and never include credentials.

Milestone state:

- [x] Author contract tests locally before implementation.
- [x] Implement strict contracts and provenance/hash helpers locally.
- [x] Run lightweight static checks locally.
- [ ] Execute the CPU-bound pytest contract suite in Kaggle or Google Colab and attach fresh output.

### Task 9: GPU notebook boundary and evaluation runtime

**Files:**
- Create later: `nhscopilot-eval/notebooks/gpu_baseline.ipynb`
- Create later: `nhscopilot-eval/src/nhscopilot_eval/providers.py`
- Create later: `nhscopilot-eval/src/nhscopilot_eval/scoring.py`
- Create later: `nhscopilot-eval/src/nhscopilot_eval/analysis.py`

The notebook is an exportable, synthetic-input-only workflow for Kaggle or Google Colab. It must not download restricted sources, expose hidden labels, persist raw provider output, or silently substitute unavailable models. Local execution remains limited to lightweight structural checks unless the user changes the explicit CPU restriction.

### Task 10: Independent local rights/model guardrails

**Files:**
- Create: `nhscopilot-eval/configs/rights_ledger.yaml`
- Create: `nhscopilot-eval/configs/models.yaml`
- Create: `nhscopilot-eval/scripts/check_offline_policy.ps1`
- Create: `nhscopilot-eval/docs/evidence/independent-guardrail-check-2026-08-18.md`
- Modify: `FLOW.md`
- Modify: `DECISIONS.md`

These artifacts do not require CPU tests, provider calls, source downloads, model downloads, or
GPU execution. The rights ledger records the synthetic fallback and blocked external candidates.
The model registry records that no model snapshot has been availability-verified and preserves
`not_run` semantics. The PowerShell guardrail checks these policies and forbidden artifacts locally.

- [x] Add the synthetic-only rights ledger without external URLs or source text.
- [x] Add a model registry with no fabricated availability or model-quality claims.
- [x] Align flow and decision records with the new guardrails.
- [x] Run the PowerShell guardrail only and record its output.
- [x] Keep the CPU pytest contract gate open for Kaggle/Colab.

### Task 11: Complete local evaluation harness

Files:
- Create: nhscopilot-eval/src/nhscopilot_eval/prompts.py
- Create: nhscopilot-eval/src/nhscopilot_eval/splits.py
- Create: nhscopilot-eval/src/nhscopilot_eval/redaction.py
- Create: nhscopilot-eval/src/nhscopilot_eval/providers.py
- Create: nhscopilot-eval/src/nhscopilot_eval/scoring.py
- Create: nhscopilot-eval/src/nhscopilot_eval/analysis.py
- Create: nhscopilot-eval/src/nhscopilot_eval/report.py
- Create: nhscopilot-eval/src/nhscopilot_eval/app.py
- Create: nhscopilot-eval/src/nhscopilot_eval/sources.py
- Create: nhscopilot-eval/src/nhscopilot_eval/adjudication.py
- Create: nhscopilot-eval/src/nhscopilot_eval/replay.py
- Create: nhscopilot-eval/scripts/build_benchmark.py
- Create: nhscopilot-eval/scripts/run_eval.py
- Create: nhscopilot-eval/scripts/score_eval.py
- Create: nhscopilot-eval/scripts/build_public_bundle.py
- Create: nhscopilot-eval/tests/test_generation_and_splits.py
- Create: nhscopilot-eval/tests/test_providers_scoring.py
- Create: nhscopilot-eval/tests/test_analysis_report_app.py
- Create: nhscopilot-eval/tests/test_governance_and_replay.py
- Create: nhscopilot-eval/docs/DATASET_CARD.md
- Create: nhscopilot-eval/docs/DISCLOSURE_CHECKLIST.md

Local implementation state:

- [x] Synthetic 100/50/50 row-generation code exists without fetching or embedding external content.
- [x] Public projection, private authoring, and sealed evaluation boundaries are explicit.
- [x] Fixture provider, unavailable state, redaction, replay, adjudication, scoring, analysis, report, and app code exist.
- [x] Offline test files and CLI scripts are authored.
- [ ] CPU tests execute and pass in Kaggle/Colab.
- [ ] Rights-sensitive sources, remote providers, publication, deployment, and model-quality claims are approved and evidenced.
