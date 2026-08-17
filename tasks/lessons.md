# tasks/lessons.md — NHSCopilot-Eval

**Review date:** 2026-08-08  
**Status:** Local implementation lessons only. Read before every future session.

**Authorization boundary:** local source creation, tests, dependencies, and synthetic evaluation are
allowed. Do not fetch restricted sources, call remote providers, publish, deploy, or send outreach
without separate approval.

## Lesson 1 — NICE content requires an AI/reuse decision

**Problem:** public NICE pages were treated as unrestricted benchmark source text.  
**Root cause:** public availability was confused with global AI/publication rights.  
**Fix:** record licence, geography, AI permission, revision, URL, anchor, and hash; keep hidden text private.  
**Guard:** Day 43 rights gate blocks authoring/public release when permission is missing.

## Lesson 2 — NICE identifiers drift and can be misassigned

**Problem:** the brief maps obsolete/wrong identifiers to topics.  
**Root cause:** no live ID/revision verification.  
**Fix:** verify NG28, NG136, NG12, NG253, and CG187 (or a documented replacement) at implementation time.  
**Guard:** reject obsolete IDs and store canonical URL plus document hash.

## Lesson 3 — BNF is not a default public AI source

**Problem:** BNF interaction text was assumed free to copy.  
**Root cause:** NHS accessibility was confused with redistribution permission.  
**Fix:** exclude BNF unless written permission covers AI and public distribution; prefer cleared MHRA sources.  
**Guard:** public-bundle scan rejects BNF markers and unapproved source IDs.

## Lesson 4 — ICD-10 has ownership and edition constraints

**Problem:** unspecified ICD-10 codes were planned for public release.  
**Root cause:** WHO/NHS licensing and UK coding standards were omitted.  
**Fix:** pin UK edition/licence privately, use synthetic vignettes, and never redistribute code tables.  
**Guard:** source manifest and coder review are required before Day 44.

## Lesson 5 — Retired or paid models cannot be silently replaced

**Problem:** Claude 3.5 and a free GPT-4o assumption were treated as stable.  
**Root cause:** aliases, deprecations, and billing were not part of the benchmark contract.  
**Fix:** exact model registry, availability/cost gate, local baseline, and not_run state.  
**Guard:** registry test fails on missing snapshot or budget and never falls back invisibly.

## Lesson 6 — Public labels leak the evaluation key

**Problem:** publishing all 200 answers before scoring enables memorization and prompt tuning.  
**Root cause:** transparency was prioritized without a hidden test design.  
**Fix:** public development metadata plus sealed private test prompts/labels.  
**Guard:** disclosure scan rejects hidden labels, answer keys, and source passages in public output.

## Lesson 7 — Medication safety is not Boolean

**Problem:** safe true/false cannot represent context or uncertainty.  
**Root cause:** clinical risk was reduced to ordinary classification.  
**Fix:** safe, unsafe, review, and insufficient-information outcomes with severity weighting.  
**Guard:** unsafe false reassurance is the primary safety metric and high-risk rows receive dual review.

## Lesson 8 — Every category needs a strict scorer

**Problem:** the brief code sketch has no medication branch and vague NICE accuracy.  
**Root cause:** scorer interface was not defined before evaluation.  
**Fix:** separate guidance, ICD-10, and medication scorers; unknown categories raise an error.  
**Guard:** fixtures cover malformed, refusal, invalid-code, fabricated-citation, and unsafe answers.

## Lesson 9 — API calls need reproducibility and redaction

**Problem:** model names alone cannot reproduce a run and raw responses can leak secrets/text.  
**Root cause:** no request metadata, hashes, retry, or logging contract.  
**Fix:** capture snapshot, endpoint, parameters, prompt/config/response hashes, cost, failures, and redacted logs.  
**Guard:** local fixture mode passes without credentials; secret scan and network-disabled app test pass.

## Lesson 10 — Small heterogeneous benchmarks cannot prove a winner

**Problem:** a single mean and prewritten Claude-leading claim overstate evidence.  
**Root cause:** no uncertainty or category-specific analysis.  
**Fix:** category macro metrics, critical safety misses, abstention, paired bootstrap intervals, and neutral claims.  
**Guard:** analysis contains no winner/threshold gate; publication requires manifest-linked claims and manual review.

Add new lessons after any implementation correction, user correction, failed gate, or source change.

## Lesson 11 — Static checks must treat manifest markers literally

Problem: the first offline checker used a PowerShell wildcard assertion for the literal YAML
marker external_sources: [], and the checker failed before evaluating project content.

Root cause: wildcard syntax was used for a value containing pattern metacharacters.

Fix: use literal Contains checks for configuration markers; use explicit line-prefix checks for
frontmatter instead of assuming a particular line-ending regex.

Guard: reusable offline checks must distinguish checker failures from project-policy failures and
must never require a test runner, package installation, network, or model execution.

## Lesson 12 — CPU test evidence must remain environment-specific

Problem: the contract suite exists locally, but the user explicitly prohibits running CPU tests in
this workspace.

Root cause: local source authoring and test execution were being treated as the same milestone.

Fix: keep test code, fixtures, and the Kaggle/Colab command runbook local; leave the execution box
unchecked until a notebook produces fresh output.

Guard: report static contract inspection separately from pytest results and never claim red-green
or passing tests without notebook evidence.
