# NHSCopilot-Eval

Provenance-aware, synthetic-first evaluation harness for NHS-oriented language-model behavior.

This repository is research tooling, not a clinical product or NHS service. It does not establish
clinical safety, regulatory compliance, NHS/NICE/MHRA/WHO endorsement, or deployment readiness.

## Current state

The local harness includes strict contracts, synthetic row-generation code, public/private/sealed
split boundaries, redaction, replay, adjudication, category scoring, paired analysis, aggregate
reporting, and an offline catalogue app.

CPU tests are authored but intentionally not run in this local workspace. Run them only in the
documented Kaggle/Colab environment: nhscopilot-eval/docs/KAGGLE_COLAB_TEST_RUN.md.

## Boundaries

- External NICE, BNF, ICD-10, WHO, NHS, and other rights-sensitive sources are not accessed.
- Remote providers, credentials, publication, deployment, and outreach remain gated.
- Unavailable models remain not_run; no model is silently substituted.
- GPU notebooks are for explicitly approved evaluation only. Project 09 does not train models.

See nhscopilot-eval/README.md, HANDOVER.md, and nhscopilot-eval/docs/DATASET_CARD.md for local
scope, provenance, limitations, and evidence.
