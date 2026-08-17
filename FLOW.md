# FLOW — NHSCopilot-Eval

Current gate: [`STATUS.md`](STATUS.md). The flow below describes the intended artifact path; the
status file identifies which stages have fresh evidence.

```text
rights ledger + execution policy + model registry
  â†’ source manifest + rights decision
  → synthetic/licence-cleared authoring
  → deterministic row_id + content hash
  → public development / private authoring / sealed evaluation split
  → strict BenchmarkRow validation
  → dual review + adjudication for ambiguous/high-severity rows
  → local baseline and optional gated providers
  → redacted result records + replay hashes
  → category scoring + abstention/error taxonomy
  → paired bootstrap uncertainty
  → disclosure-reviewed aggregate bundle
  → offline catalogue app
```

The current local implementation has generated the synthetic rows through the deterministic
generator. It has not fetched sources, called providers, evaluated a model, or published results.
The generated JSONL remains ignored local development data.

The local implementation keeps rights, execution, and model availability decisions outside row
authoring. The contract pytest suite is authored but runs only in Kaggle/Google Colab; local
PowerShell checks do not execute pytest, providers, models, or network calls. Lightweight Python
generation is allowed and separately evidenced.
