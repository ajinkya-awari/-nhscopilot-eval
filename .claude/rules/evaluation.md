---
paths:
  - "src/nhscopilot_eval/scoring.py"
  - "src/nhscopilot_eval/analysis.py"
  - "src/nhscopilot_eval/providers.py"
  - "tests/**/*.py"
---

# Evaluation Rules

- Require exactly 200 validated rows with category and split checks.
- Run a local baseline without credentials before optional providers.
- Keep unavailable models as `not_run`; never silently substitute.
- Keep refusals, abstentions, malformed outputs, timeouts, provider errors, and insufficient information distinct.
- Use locked paired rows and bootstrap uncertainty; never prewrite a winner.
- Hash requests/configuration for replay without exposing secrets.
