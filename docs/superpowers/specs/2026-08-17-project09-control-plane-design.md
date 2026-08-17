# Project 09 Control Plane Design

**Status:** Approved by user on 2026-08-17.

**Implementation status:** The control plane and local source boundary are complete and pushed to
GitHub with user authorization. The next open gate is Kaggle/Colab contract-test evidence; this
spec does not authorize provider calls, rights-sensitive source access, benchmark publication, or
deployment.

## Goal

Create a self-contained Codex and Claude Code operating system for NHSCopilot-Eval that preserves provenance, licensing, privacy, hidden-test, safety, replay, and disclosure requirements across sessions.

## Design

Root `AGENTS.md` is the Codex bootstrap and `CLAUDE.md` is the project brain. Both point to the same authority chain and living collaboration records. `.claude/` contains six NHS-evaluation specialists, three commands, two local guardrail hooks, three path-aware rules, one workflow skill, and project-scoped settings.

The 15 prompt files retain the requested categories but are rewritten for provenance-led benchmark work. The AI Collaboration Field Guide becomes `HANDOVER.md`, `DECISIONS.md`, `FLOW.md`, `ARCHITECTURE.md`, `CONSTRAINTS.md`, `TEST_CHECKLIST.md`, `ROLLBACK.md`, and bug/feature templates.

## Safety Boundaries

Local synthetic work is authorized. Rights-sensitive source access, provider calls, remote execution, deployment, publication, and outreach remain separate approval gates. The repository push was separately user-authorized; hooks never upload, publish, contact providers, or read secret values.

## Verification

- Confirm all expected files exist and are non-empty.
- Parse `.claude/settings.json`.
- Validate all six agent frontmatter blocks.
- Confirm all 15 prompts mention only NHSCopilot-Eval domain terms.
- Search for unrelated portfolio terminology, stale freeze text, fabricated scores, and secrets.
