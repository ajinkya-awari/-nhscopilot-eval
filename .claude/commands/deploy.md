---
name: deploy
argument-hint: [target]
---

Prepare, but do not execute, an NHSCopilot-Eval catalogue deployment.

1. Read `CONSTRAINTS.md`, `ROLLBACK.md`, and disclosure evidence.
2. Confirm the app reads frozen aggregates only, has no provider keys, and shows research-only disclaimers.
3. Run offline smoke, secret/PHI/restricted-content scans, and aggregate-manifest parity checks.
4. Produce exact dry-run commands and stop before any network, hosting, publication, or public release.
5. Require explicit user approval before external action.
