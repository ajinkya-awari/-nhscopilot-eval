# Kaggle/Colab contract-test run

This is a runbook for the CPU-bound contract tests. It is not an instruction to run tests in the
local Windows workspace.

## Preconditions

- Use a Kaggle notebook or Google Colab runtime with Python 3.12.
- Upload or otherwise make the local nhscopilot-eval source boundary available to the notebook.
- Use only the synthetic fixtures in tests/fixtures.
- Do not add credentials, provider calls, restricted source text, patient data, hidden labels, or
  raw model outputs.

## Commands

From the nhscopilot-eval directory in the notebook:

    python -m pip install -e ".[verification]"
    python -m pytest -q tests/test_contracts.py

Expected scope: the contract tests only. Record the Python version, package versions, command,
exit code, and complete output in a dated evidence file. Do not convert an expected result into a
claim before the notebook produces fresh output.

## Current local status

- Test file authored: tests/test_contracts.py
- Test execution: intentionally not run locally by user constraint
- Providers: disabled
- GPU model execution: not part of this contract-test milestone
- Rights-sensitive sources: not accessed
