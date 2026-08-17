# CONSTRAINTS — NHSCopilot-Eval

## Never Do Automatically

- Do not read or print `.env`, keys, tokens, PHI, patient records, or hidden labels.
- Do not fetch NICE, BNF, ICD-10, WHO, NHS, or other rights-sensitive material without a recorded rights decision.
- Do not redistribute BNF text, WHO/NHS code tables, or restricted guideline text.
- Do not use the example scores in `PROJECT_BRIEF.md` as results.
- Do not silently replace an unavailable or retired model.
- Do not call providers in offline tests or dry runs.
- Do not store raw provider outputs, hidden reasoning, or prompt traces in public artifacts.
- Do not claim clinical safety, endorsement, or deployment readiness.
- Do not deploy, publish, email, push Git, or force-push without approval.

## Required Gates

- Rights ledger and source manifest before content use.
- Exactly 200 validated rows with deterministic IDs and hashes.
- Public/private/sealed split and leakage checks.
- Dual review plus adjudication for ambiguous/high-severity rows.
- Local baseline before optional providers.
- Replay, secret, PHI, and disclosure scans before any release.
