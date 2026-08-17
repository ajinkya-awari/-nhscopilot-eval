# Project 09 status — read this first

**As of:** 2026-08-18
**Repository:** [ajinkya-awari/-nhscopilot-eval](https://github.com/ajinkya-awari/-nhscopilot-eval)
**Remote commit:** `0952d75 feat: complete offline synthetic workflow`
**Branch state:** `main` is clean and synchronized with `origin/main`.

This is the canonical session handoff. `HANDOVER.md` contains the detailed narrative; `tasks/todo.md`
contains the gate checklist; this file gives the shortest reliable answer to “what is done and what
is next?”

## Done and evidenced

- The separate `nhscopilot-eval/` source boundary exists and is pushed to GitHub.
- The local harness contains strict contracts, deterministic provenance, synthetic row generation,
  public/private/sealed split handling, redaction, fixture/unavailable providers, guarded remote
  adapter code, scoring, analysis, replay, adjudication, reporting, catalogue UI, and CLI scripts.
- A lightweight local generation run produced exactly 200 synthetic rows: 100 guidance, 50
  synthetic ICD-10, and 50 medication-safety rows.
- Generated split counts are `public_development=100`, `private_authoring=51`, and
  `sealed_evaluation=49`.
- PowerShell offline-policy and public-disclosure scans passed.
- No model was downloaded, no provider was called, no model was trained or inferred locally, and
  no CPU-heavy test suite was run.
- The generated JSONL and Python cache are ignored local artifacts; private/sealed labels and raw
  outputs were not pushed.

Evidence: [lightweight generation](<E:/application/MS CS/portfolio-projects/09-nhscopilot-eval/nhscopilot-eval/docs/evidence/lightweight-generation-check-2026-08-18.md>),
[documentation consistency](<E:/application/MS CS/portfolio-projects/09-nhscopilot-eval/nhscopilot-eval/docs/evidence/documentation-consistency-check-2026-08-18.md>),
[HANDOVER](<E:/application/MS CS/portfolio-projects/09-nhscopilot-eval/HANDOVER.md>), and
[offline guardrail](<E:/application/MS CS/portfolio-projects/09-nhscopilot-eval/nhscopilot-eval/scripts/check_offline_policy.ps1>).

## Next exact task

Run the authored contract tests in Kaggle or Google Colab only, using
[KAGGLE_COLAB_TEST_RUN.md](<E:/application/MS CS/portfolio-projects/09-nhscopilot-eval/nhscopilot-eval/docs/KAGGLE_COLAB_TEST_RUN.md>):

```text
python -m pytest -q tests/test_contracts.py
```

Record Python/package versions, the complete output, exit code, and a dated evidence file. Do not
run this command in the local Windows workspace.

## Pending after the notebook test

1. Complete two independent reviews and adjudication for ambiguous/high-severity synthetic rows.
2. Freeze public metadata and private/sealed manifests with hashes.
3. Keep NICE/BNF/ICD-10 rights decisions open; no restricted source access is needed for the
   synthetic fallback.
4. Select and verify an exact local model snapshot before any model evaluation.
5. Run model evaluation only in an approved notebook with synthetic inputs and recorded cost and
   availability metadata.
6. Run the network-disabled app smoke test and final disclosure/claims review in the approved
   environment.

Benchmark publication, deployment, outreach, clinical-facing claims, and external source/provider
access remain blocked. The GitHub repository push was explicitly authorized by the user and is
complete; repository publication is not benchmark or clinical approval.

## Non-negotiable execution rule

Local work may use lightweight offline generation and PowerShell/static checks. Do not download
models or packages, call providers, train/infer models, or run CPU-heavy tests locally. Keep all
CPU-bound pytest and GPU/model work in Kaggle or Google Colab.

## Read order next session

1. `STATUS.md`
2. `AGENTS.md` and `CLAUDE.md`
3. `HANDOVER.md`, `DECISIONS.md`, `FLOW.md`, and `tasks/todo.md`
4. The implementation plan and newest evidence file
5. The exact file named by the next unchecked gate
