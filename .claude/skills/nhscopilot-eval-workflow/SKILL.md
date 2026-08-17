---
name: nhscopilot-eval-workflow
description: Apply the Project 09 provenance-first workflow to NHS-oriented benchmark, scoring, provider, safety, and disclosure tasks.
user-invocable: true
---

1. Read `AGENTS.md`, `CLAUDE.md`, `HANDOVER.md`, `DECISIONS.md`, `CONSTRAINTS.md`, and the authority chain.
2. Identify the next rights, data, safety, or evaluation gate in `tasks/todo.md`.
3. Record sources, licences, versions, hashes, and split impact before authoring data.
4. Use synthetic fixtures and offline mode before any provider call.
5. Validate strict contracts and public/private/sealed disjointness.
6. Run local baseline first; represent unavailable providers as `not_run`.
7. Keep refusal, abstention, malformed, timeout, provider error, and insufficient-information outcomes separate.
8. Compute category metrics and paired uncertainty on locked rows only.
9. Run secret, PHI, restricted-content, replay, and disclosure scans.
10. Stop at rights-sensitive access, provider calls, deployment, publication, email, and Git push gates.

Ask the user before external actions or changes to rights, hidden labels, public claims, or model registry semantics. Infer routine local validation from the project files.
