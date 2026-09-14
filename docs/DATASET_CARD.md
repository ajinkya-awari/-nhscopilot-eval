# NHSCopilot-Eval Dataset Card

## Status

This public repository contains synthetic fixtures for software-contract testing. It does not release a benchmark dataset, hidden labels, provider responses, model outputs, patient records, or clinical/NHS data.

The public synthetic-contract scope is complete with limitations: local source tests passed 97 tests, and the current public package passed 33 tests on private Kaggle CPU. Research execution is not released.

## Scope

The public fixtures exercise schema validation, malformed-response rejection, prompt-as-data handling, redaction boundaries, replay hashes, provider-unavailable states, and scoring/reporting contracts.

The original development tree included deterministic toy private/sealed labels in earlier public history. Those toy labels are considered exposed and cannot support held-out benchmark claims.

## Provenance And Rights

The current fallback uses independently authored synthetic prompts only. NICE, BNF, ICD-10, WHO, NHS, and other rights-sensitive source text is not admitted into this public package. Any future external source requires URL, version/date, license decision, AI/reuse decision, content hash, and citation anchor before authoring or release.

## Safety And Privacy

This project is research tooling, not clinical advice or a clinical product. It must not contain patient identifiers, clinical records, raw provider responses, hidden reasoning, credentials, hidden labels, or restricted source passages.

## Evaluation Limits

The fixture provider and scorers are implementation checks. They do not measure medical correctness, clinical safety, source validity, provider quality, deployment readiness, regulatory compliance, or institutional endorsement.

Replacement rows, independent review, frozen manifests, provider/model evidence, benchmark publication, deployment review, and clinical/NHS/regulatory review remain open gates.
