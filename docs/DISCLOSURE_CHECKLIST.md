# Disclosure checklist

Current state: the public synthetic-contract package is complete with limitations. The public
export contains source code, tests, synthetic fixtures, configuration, license, notices, citation
metadata, and runbook material. It does not contain private control-plane records, provider
responses, private or sealed labels, raw clinical text, model files, or credentials.

- [x] Public package excludes private authoring files, sealed labels, raw provider responses, and hidden reasoning.
- [x] Public tests exercise schema validation, malformed-response rejection, prompt-as-data handling, unavailable-provider states, redaction, scoring, reporting, and replay contracts.
- [x] `not_run`, refusal, abstention, timeout, malformed, and provider-error states are distinct in the contracts.
- [x] Secret, private-path, AI-residue, sibling-project, cache, model/checkpoint, unsupported-claim, clinical-data indicator, and local Markdown-link scans passed for this export.
- [x] BNF, restricted guideline text, WHO/NHS code tables, clinical records, and patient identifiers are absent from the public package.
- [x] Research-only and not-clinical-advice boundaries are visible in README, dataset card, reports, and app output.
- [ ] Pinned dependency lock and full source-suite target-runtime evidence remain open.
- [ ] Replacement synthetic rows require independent review before benchmark use.
- [ ] Model/provider snapshots, availability, cost, and parameters remain unrecorded because provider/model evaluation is not released.
- [ ] Benchmark publication, deployment, outreach, and clinical/NHS/regulatory review require separate approval and evidence.
