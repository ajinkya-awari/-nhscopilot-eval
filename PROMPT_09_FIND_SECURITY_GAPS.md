# Prompt 09 — Find Security Gaps

Audit the authorized NHSCopilot-Eval repository as an attacker.

Check secrets in code/config/history, PHI and patient identifiers, NICE/BNF/ICD-10/WHO/NHS text leakage, hidden labels, prompt injection, unsafe parsing, path traversal, oversized inputs, provider-output retention, model substitution, retry/cost abuse, error leakage, public-app network access, and endorsement claims. Rank findings with exact file/line, fix critical local issues only, and leave external actions as gated tickets.
