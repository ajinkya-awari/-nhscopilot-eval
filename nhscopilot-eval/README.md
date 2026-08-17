# NHSCopilot-Eval source boundary

This directory is the separate local source boundary for Project 09. The parent directory remains
the planning and control-plane folder.

Read the parent [`STATUS.md`](../STATUS.md) before working here; it identifies the current gate,
done evidence, and the exact next action.

The local implementation now contains:

- synthetic-authorship fallback provenance;
- deterministic synthetic row authoring for the 100/50/50 target;
- public/private/sealed split and public projection boundaries;
- strict Pydantic contracts, redaction, replay, adjudication, scoring, and analysis modules;
- a local fixture provider and explicit unavailable-model semantics;
- an SDK-neutral guarded remote adapter that remains `not_run` until explicit opt-in and budget metadata;
- aggregate-only reporting and a frozen catalogue app; and
- public/private/sealed directory boundaries; and
- an execution policy that keeps local work offline and defers GPU-dependent model work to an
  explicitly approved Kaggle or Google Colab notebook.

The lightweight local workflow may generate the 200 synthetic rows and scan the public projection.
Generated private/sealed JSONL remains ignored and is never a release artifact. Use
`scripts/check_disclosure.ps1` before any user-reviewed bundle is considered for publication.

No clinical advice, NHS/NICE/MHRA/WHO endorsement, safety claim, deployment claim, provider call,
restricted source text, patient data, hidden labels, or benchmark metric is claimed here.

The test suite is authored but must be run only in Kaggle or Google Colab per the project execution
policy. Local PowerShell checks do not run pytest, providers, models, or network calls. The small
deterministic generator is the only lightweight Python workflow currently evidenced locally.

Project 09 is an evaluation harness. GPU notebooks may be used for explicitly selected model
evaluation, but model training is out of scope.

The source boundary must not be populated from BNF text, WHO/NHS code tables, patient records, or
other restricted/licence-sensitive material. External sources require a recorded rights decision
before authoring.
