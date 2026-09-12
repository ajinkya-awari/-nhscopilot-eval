# Future target-runtime verification (gated)

This runbook is for a later authorized Kaggle or Colab synthetic-only test. It was not executed during the 2026-09-12 local audit. Do not upload private or sealed rows, credentials, provider outputs, medical records, restricted source text, models, or checkpoints.

After explicit authorization, select only the public-export files and verify that the runtime uses Python 3.12. Record package versions, device, date, exact commands, full output, exit codes, and an evidence path. From the public export root in that runtime:

```powershell
python -m pip install -e ".[verification]"
python -m compileall -q src scripts tests examples
python -m pytest -q
python examples/offline_fixture.py
```

Stop on installation or test failure and record the blocker. These commands are contract and fixture checks only; they do not authorize a provider call, model inference, dataset download, benchmark publication, or deployment.
