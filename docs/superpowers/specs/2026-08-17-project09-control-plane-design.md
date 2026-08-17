# Project 09 Control Plane Design

**Status:** Approved by user on 2026-08-17.

## Goal

Create a self-contained Codex and Claude Code operating system for NHSCopilot-Eval that preserves provenance, licensing, privacy, hidden-test, safety, replay, and disclosure requirements across sessions.

## Design

Root `AGENTS.md` is the Codex bootstrap and `CLAUDE.md` is the project brain. Both point to the same authority chain and living collaboration records. `.claude/` contains six NHS-evaluation specialists, three commands, two local guardrail hooks, three path-aware rules, one workflow skill, and project-scoped settings.

The 15 prompt files retain the requested categories but are rewritten for provenance-led benchmark work. The AI Collaboration Field Guide becomes `HANDOVER.md`, `DECISIONS.md`, `FLOW.md`, `ARCHITECTURE.md`, `CONSTRAINTS.md`, `TEST_CHECKLIST.md`, `ROLLBACK.md`, and bug/feature templates.

## Safety Boundaries

Local synthetic work is authorized. Rights-sensitive source access, provider calls, remote execution, deployment, publication, outreach, and Git push remain separate approval gates. Hooks never upload, publish, contact providers, or read secret values.

## Verification

- Confirm all expected files exist and are non-empty.
- Parse `.claude/settings.json`.
- Validate all six agent frontmatter blocks.
- Confirm all 15 prompts mention only NHSCopilot-Eval domain terms.
- Search for unrelated portfolio terminology, stale freeze text, fabricated scores, and secrets.
