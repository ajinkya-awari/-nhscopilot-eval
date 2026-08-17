---
name: fix-issue
argument-hint: [issue-number-or-bug-file]
---

Fix the specified NHSCopilot-Eval issue.

1. Read `HANDOVER.md`, `CONSTRAINTS.md`, and the issue record.
2. Reproduce with a synthetic fixture and capture the full error.
3. Write a regression test that fails before the fix.
4. Implement the smallest root-cause fix without changing locked labels or row IDs.
5. Run focused tests in the approved Kaggle/Colab environment; do not run CPU-heavy tests locally.
6. Update `BUG_TEMPLATE.md`, `DECISIONS.md`, `HANDOVER.md`, and `tasks/lessons.md`.
7. Do not access restricted sources, call providers, publish, deploy, or commit automatically.
