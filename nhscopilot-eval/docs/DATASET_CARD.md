# NHSCopilot-Eval dataset card

## Status

Local synthetic authoring scaffold. No public release, provider evaluation, clinical claim, or
institutional endorsement is made by this file.

## Scope

The planned benchmark contains 100 guidance-comprehension rows, 50 synthetic coding rows, and 50
medication-safety communication rows. Public development metadata, private authoring data, and
sealed evaluation labels remain separate.

## Provenance and rights

The current fallback uses independently authored synthetic prompts only. External NICE, BNF,
ICD-10, WHO, NHS, and other rights-sensitive content has not been accessed or admitted. Any future
external source requires a URL, version/date, licence decision, AI/reuse decision, content hash,
and citation anchor before authoring or release.

## Safety and privacy

The benchmark is research tooling, not clinical advice or a clinical product. It must not contain
patient records, PHI, hidden labels in public artifacts, raw provider responses, hidden reasoning,
keys, or restricted source passages. Medication rows use uncertainty and escalation labels rather
than a binary safety claim.

## Evaluation

The local fixture provider and scorers are implementation fixtures. CPU test execution is deferred
to Kaggle or Google Colab. No model-quality metric is claimed until a locked run produces reviewed
evidence.

## Limitations

Synthetic rows do not establish real-world clinical validity. Small heterogeneous benchmarks cannot
prove model safety, deployment readiness, regulatory compliance, or NHS/NICE/MHRA/WHO endorsement.
