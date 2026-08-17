# AGENTS.md — Project 09 NHSCopilot-Eval

This is the Codex project instruction contract. Codex reads `AGENTS.md` before work. Keep it aligned with `CLAUDE.md`; do not merge instructions from another portfolio project.

## Session Start

1. Read this file and `CLAUDE.md`.
2. Read `HANDOVER.md`, `DECISIONS.md`, `ARCHITECTURE.md`, `CONSTRAINTS.md`, `FLOW.md`, and `tasks/lessons.md`.
3. Read `DESIGN.md`, `FINAL_VULNERABILITY_SCAN.md`, and `CLAUDE_CODE_PROMPT.md` in that order.
4. Read `tasks/todo.md` and identify the next unchecked rights, data, safety, or evaluation gate.
5. Inspect the current diff before editing.

## Workflow Orchestration

### Plan Mode Default

- Enter plan mode for any task with three or more steps or an architectural decision.
- Stop and re-plan when rights, data, model availability, or evaluation evidence contradicts the plan.
- Use plan mode for verification, not only implementation.

### Subagent Strategy

- Use one focused specialist per independent evidence lane.
- Keep provenance, dataset authoring, provider adapters, scoring, and disclosure review isolated.
- Never let parallel work share hidden labels, private manifests, or mutable generated bundles.

### Self-Improvement Loop

- Record every correction and failed assumption in `tasks/lessons.md`.
- Add a prevention rule and affected artifact, not only a narrative.

### Verification Before Done

- Require fresh command output and an evidence path before marking any gate complete.
- Read the full diff and check public/private/sealed split boundaries.
- Never claim clinical safety, NHS endorsement, or deployment readiness.

### Demand Elegance

- Prefer explicit provenance and typed contracts over clever heuristics.
- Keep rights, data, provider, scoring, and publication decisions independently reviewable.

### Autonomous Bug Fixing

- Reproduce with synthetic fixtures, prove the root cause, and add a regression test.
- Keep unavailable providers as `not_run`; never silently substitute a model.

## Task Management

- Track work in `tasks/todo.md`.
- Record rationale in `DECISIONS.md` and state in `HANDOVER.md`.
- Update `FLOW.md` when data or artifact flow changes.
- End every session with a five-line handoff summary.

## Project Boundaries

- Project 09 is an evaluation harness, not a clinical product or NHS service.
- This folder is the planning/control-plane folder; the future `nhscopilot-eval/` source repository is a separate boundary.
- Local documentation, source creation, dependencies, tests, and local synthetic evidence are authorized.
- Provider calls require explicit opt-in, budget, availability, and synthetic-input checks.
- Never fetch or redistribute BNF text, WHO/NHS code tables, PHI, patient records, or restricted guideline text.
- Never expose hidden labels, raw provider outputs, keys, prompt traces, or private manifests.
- Never deploy, publish, email, push Git, or imply endorsement without explicit approval.
- Do not auto-commit or force-push.

## Required New-Session Response

Summarize the current gate, rights/data status, files to touch, verification commands, and external actions that remain closed. Wait for approval for non-trivial work.
