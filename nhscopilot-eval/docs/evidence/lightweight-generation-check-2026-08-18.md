# Lightweight local generation evidence — 2026-08-18

## Scope

This evidence covers only deterministic synthetic-row generation and public-surface disclosure
checking. No package installation, model download, provider call, model inference, training, or
CPU-heavy test runner was used.

## Commands

```powershell
$env:PYTHONPATH='src'
$env:PYTHONDONTWRITEBYTECODE='1'
python scripts/build_benchmark.py
& .\scripts\check_offline_policy.ps1
& .\scripts\check_disclosure.ps1
```

The source tree was used directly through `PYTHONPATH`; dependencies were not installed.

## Observed output

```text
COUNTS guidance=100, icd10_synthetic=50, medication_safety=50
SPLITS private_authoring=51, public_development=100, sealed_evaluation=49
OFFLINE POLICY CHECK: PASS
PUBLIC DISCLOSURE SCAN: PASS
CPU-heavy tests/model inference/network execution: NOT USED
```

## Boundary

The generated private and public JSONL files remain local and ignored by Git. Hidden answer keys,
sealed rows, raw provider output, adjudication records, and restricted source text were not
released. This evidence does not establish model quality, clinical safety, NHS endorsement, or
regulatory compliance.
