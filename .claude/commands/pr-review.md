---
name: pr-review
argument-hint: [base-ref]
---

Review an NHSCopilot-Eval change against the research contracts.

1. Read the complete diff from the requested base.
2. Check rights, provenance, public/private/sealed separation, schema, scoring, replay, safety, and disclosure.
3. Run offline contract, split, scoring, replay, and app tests.
4. Report CRITICAL / WARNING / SUGGESTION with exact file and line.
5. Do not approve, commit, push, deploy, publish, or contact providers on the user's behalf.
