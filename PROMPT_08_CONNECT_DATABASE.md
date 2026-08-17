# Prompt 08 — Connect Your Database

Assess whether the NHSCopilot-Eval feature needs persistence.

Default to local manifests, JSONL results, and reproducible aggregate files. If a database is genuinely required, specify schema, indexes, migrations, rollback, retention, access controls, redaction, and tests. Never store PHI, restricted source text, hidden labels, or raw provider outputs in a hosted database. Prove local synthetic read/write behavior before any external connection.
