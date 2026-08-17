# FLOW — NHSCopilot-Eval

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

The current control-plane task changes only documentation and guardrails. It does not create rows, fetch sources, call providers, or publish results.

The local implementation scaffold now keeps rights, execution, and model availability decisions
outside row authoring. The contract pytest suite is authored but runs only in Kaggle/Google Colab;
local PowerShell checks do not execute Python, providers, models, or network calls.
