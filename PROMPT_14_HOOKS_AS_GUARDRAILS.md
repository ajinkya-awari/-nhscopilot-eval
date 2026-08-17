# Prompt 14 — Hooks as Guardrails

Audit or create the Project 09 NHSCopilot-Eval `.claude` guardrails.

Keep hooks short, deterministic, local, and Windows-aware. Pre-commit may run compile/tests and block failures. Post-edit checks may parse JSON and scan likely secret markers. Hooks must not read secret values, access restricted sources, call providers, upload, publish, delete broadly, commit, push, email, or deploy. Trigger checks safely and show output.
