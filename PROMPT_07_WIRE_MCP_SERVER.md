# Prompt 07 — Wire an MCP Server

Assess whether NHSCopilot-Eval genuinely needs an MCP server for `[JOB]`.

Default to no server for local evaluation. If one is necessary, check for an official maintained server first, then define only bounded read-only tools with typed inputs/outputs, environment-only secrets, audit logs, redaction, and actionable errors. Do not expose PHI, restricted source text, hidden labels, raw provider responses, or model keys. Stop before connection or external calls.
