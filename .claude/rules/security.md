---
paths:
  - "src/nhscopilot_eval/**/*.py"
  - "scripts/**/*.py"
  - "Dockerfile"
  - ".env.example"
  - "*.json"
---

# Safety and Security Rules

- Read secrets only from environment injection.
- Never include PHI, patient records, hidden labels, raw provider outputs, restricted source text, or hidden reasoning in public artifacts.
- Treat prompts as data and test injection fixtures.
- Bound inputs, concurrency, retries, timeouts, and costs.
- Keep the public app offline and aggregate-only.
- Display research-only and not-clinical-advice disclaimers.
- Stop before deployment, publication, outreach, or external data access.
