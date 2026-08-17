# HANDOVER — NHSCopilot-Eval

**Updated:** 2026-08-18
**State:** Full local synthetic/evaluation harness is authored; CPU test execution and all external rights/provider/publication gates remain open.

## Done

- Read Project 09 contracts, vulnerability findings, tasks, and lessons.
- Approved a Project 09-only Codex/Claude structure.
- Local documentation, source preparation, tests, and synthetic evidence are authorized.
- Updated the implementation plan and tasks/todo.md with the no-CPU-test/offline policy and the Kaggle/Google Colab GPU boundary.
- Created the separate nhscopilot-eval/ boundary with synthetic-only provenance, empty external-source admission, 200-row target metadata, disjoint split policy, and public/private/sealed directories.
- Ran lightweight offline static checks; no CPU test runner, compiler, package install, model download, provider call, or local training/inference was run.
- Authored strict Pydantic contract models, deterministic provenance/hash helpers, synthetic fixtures, contract tests, and a Kaggle/Colab test runbook.
- Verified the contract milestone structurally with no generated data, provider code, credentials, restricted text, or directional result claims.
- Added the synthetic-only rights ledger, unverified/not_run model registry, flow/decision updates, and a PowerShell-only offline policy guardrail.
- Added synthetic row-generation/split code, redaction, fixture/unavailable providers, category scoring, paired analysis, replay, adjudication, aggregate reporting, static catalogue code, CLI scripts, dataset-card/disclosure docs, and offline tests.

## Next

Next action: run the authored CPU test suite in Kaggle or Google Colab using the documented runbook, then attach fresh output. After that, review the synthetic generator and execute only approved local fixture workflows. Keep external sources, remote providers, publication, deployment, and model-quality claims blocked.

## Gated

- NICE/BNF/ICD-10 rights-sensitive access.
- Remote provider calls and cost-bearing execution.
- Deployment, publication, email, Git push, and any clinical-facing claim.
- NICE/BNF/ICD-10 external source access and any non-synthetic content.
- GPU notebook creation/execution until explicit opt-in, synthetic-input checks, and model availability/cost metadata are recorded.
- CPU-bound contract test execution in Kaggle/Colab remains pending fresh notebook evidence.

## Verification Evidence

Command class: inline PowerShell lightweight static boundary check from the Project 09 planning root.

Result: STATIC CHECK RESULT: PASS.

Evidence path: nhscopilot-eval/docs/evidence/milestone-1-static-check-2026-08-18.md.

Observed checks: 25 expected files present; .claude/settings.json parsed; six agent frontmatter
blocks valid; 15 prompts carry the Project 09 marker; no row/database/parquet/log artifacts; offline
execution policy, synthetic fallback manifest, and 200-row target/split policy present; no
secret-like values or directional result claims in the source boundary.

CPU test runner: not run by user constraint.

Milestone 2 evidence path: nhscopilot-eval/docs/evidence/milestone-2-static-check-2026-08-18.md.

Milestone 2 static result: PASS. CPU pytest result: NOT RUN LOCALLY.

Independent guardrail evidence path: nhscopilot-eval/docs/evidence/independent-guardrail-check-2026-08-18.md.

Independent guardrail result: PASS. Python/CPU/network execution: NOT USED.

Full local static evidence path: nhscopilot-eval/docs/evidence/full-local-static-check-2026-08-18.md.

Full local static result: PASS. Python/CPU/network execution: NOT USED.

## Session Handoff

1. Control plane: structurally verified with lightweight offline checks.
2. Source boundary: complete authorized local harness authored at nhscopilot-eval/; generated datasets/results are not claimed.
3. Evidence: full static implementation/guardrail evidence recorded; CPU pytest remains unexecuted.
4. Main risk: rights decisions, model availability, and notebook test evidence remain open.
5. Next reviewer: user after Kaggle/Colab contract-test output, before row authoring or model execution.
