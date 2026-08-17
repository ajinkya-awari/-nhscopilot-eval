# Prompt 12 — Clean Up Dead Code

Find dead code in the NHSCopilot-Eval source repository only after offline tests pass.

Search imports, dynamic references, manifests, CLI usage, docs, fixtures, public-bundle generation, provider registry, scoring categories, and replay paths before deletion. Never delete rights checks, hidden-split protections, redaction, `not_run` handling, uncertainty calculations, or disclosure scans without approval. Delete in small batches and report uncertain findings.
