# Target Runtime Runbook

This runbook is for a future authorized target-runtime check. The current public synthetic-contract scope is already complete with limitations: private Kaggle CPU version 3 passed 33 tests in 1.92s on Python 3.12.13, compile passed, and the offline fixture completed. That run did not call providers, execute models, download data or models, use GPU, access clinical/NHS data, or publish a benchmark.

## Current Verified Public Contract

```text
Kaggle kernel: ajinkya1225/nhscopilot-eval-synthetic-contracts-cpu-2026-09-13
Status: COMPLETE
Tests: 33 passed in 1.92s
Compile: passed
Provider calls: disabled
Model execution/training: disabled
Clinical/NHS data: none
```

## Future Gated Full-Source Check

The full private 97-test source suite under exact pinned dependencies remains a separate gate. Do not upload private/sealed rows, credentials, provider outputs, medical records, restricted source text, models, or checkpoints.

After explicit authorization, use only a reviewed upload manifest and record Python version, package versions, device, date, exact commands, full output, exit codes, and evidence path.

From the public export root:

```powershell
python -m pip install -e ".[verification]"
python -m compileall -q src scripts tests examples
python -m pytest -q
python examples/offline_fixture.py
```

Stop on installation or test failure and record the blocker. These commands are contract and fixture checks only; they do not authorize provider calls, model inference, dataset downloads, benchmark publication, deployment, or clinical claims.
