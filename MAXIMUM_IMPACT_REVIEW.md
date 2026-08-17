# MAXIMUM_IMPACT_REVIEW.md — NHSCopilot-Eval

**Project:** 09 NHSCopilot-Eval  
**Review date:** 2026-08-08  
**Verdict:** The brief becomes high-impact only when it is a provenance-aware, risk-calibrated
evaluation suite rather than a model popularity leaderboard. Ten of ten scan areas required fixes.

**Portfolio isolation:** Project 09 evaluates models only. It does not train ClinicalBERT (08),
perform protein fine-tuning, own general safety/bias research, or build a separate retrieval system.

## Source Inspection Summary

The brief was compared with NICE licensing pages, NHS England ICD-10 licensing material, MHRA
public safety sources, provider model/deprecation documentation, and the earlier portfolio authorization state.
The original four-model table and “Claude leads” conclusion were rejected as unsupported.

## Finding 1 — NICE rights

**Assumption:** public PDFs can be copied into a public AI benchmark.  
**Reality:** reuse is licence-, geography-, and third-party-content-dependent; AI use may require
permission.  
**Fix:** licence ledger, metadata/hashes, independently authored prompts, private hidden answers.  
**Impact:** Critical.

## Finding 2 — BNF

**Assumption:** BNF interaction data is public and redistributable.  
**Reality:** BNF-derived content requires permission and is not a default open source.  
**Fix:** exclude BNF; use licence-cleared MHRA/regulatory sources.  
**Impact:** Critical.

## Finding 3 — ICD-10

**Assumption:** ICD-10 codes can be placed in a public dataset without a release decision.  
**Reality:** WHO copyright and NHS England licence constraints apply.  
**Fix:** pin UK edition privately, synthetic vignettes, no code-table redistribution, coder review.  
**Impact:** Critical.

## Finding 4 — Models

**Assumption:** GPT-4o, Claude 3.5 Sonnet, Llama-3-70B, and Mistral-7B are stable free APIs.  
**Reality:** Claude 3.5 snapshots are retired and GPT-4o API use is paid.  
**Fix:** exact model registry, local baseline, optional cost-gated adapters, not_run status.  
**Impact:** High.

## Finding 5 — Leakage

**Assumption:** publishing all questions and answers improves transparency.  
**Reality:** it leaks the evaluation key and enables prompt tuning/memorization.  
**Fix:** public development metadata plus sealed private test labels/prompts.  
**Impact:** Critical.

## Finding 6 — Scoring

**Assumption:** one accuracy score and a boolean medication label are adequate.  
**Reality:** coding, guidance, and medication harm have different error structures; the brief also
omits the medication scorer branch.  
**Fix:** strict category scorers, severity-weighted false-negative safety metric, explicit failures.  
**Impact:** Critical.

## Finding 7 — Review and claims

**Assumption:** manually verified answers establish reliability.  
**Reality:** reviewer roles, disagreement, adjudication, and clinical disclaimer are absent.  
**Fix:** dual review for high-risk rows, adjudication ledger, research-only claims.  
**Impact:** High.

## Finding 8 — Reproducibility/security

**Assumption:** SDK calls are reproducible by model name.  
**Reality:** aliases, prompts, endpoints, parameters, costs, and logs drift.  
**Fix:** request/config hashes, fixed parameters, redaction, secret scanning, bounded retries.  
**Impact:** High.

## Finding 9 — Statistics

**Assumption:** a single overall mean identifies the best model.  
**Reality:** heterogeneous categories and 200 rows make ranking unstable.  
**Fix:** category macro metrics, paired bootstrap intervals, failures, abstentions, no winner gate.  
**Impact:** High.

## Finding 10 — Public impact

**Assumption:** push the full dataset and live API leaderboard to Hugging Face.  
**Reality:** labels, keys, source rights, and unintended live inference can leak.  
**Fix:** static aggregate-first bundle, disclosure scan, network-disabled app, manual release.  
**Impact:** High.

## Compatibility Matrix

| Component | Planning contract | Gate |
|---|---|---|
| Python | 3.12.10 Windows-compatible | Record interpreter hash |
| Core stack | datasets 3.6.0, gradio 5.49.1, numpy 2.2.6, pandas 2.2.3, pydantic 2.11.7, httpx 0.28.1, scikit-learn 1.6.1, pyyaml 6.0.2 | Clean import and lock verification |
| Providers | Optional openai 1.82.0, anthropic 0.52.0, huggingface_hub 0.31.4 | Exact snapshot availability, terms, cost |
| Sources | NICE, MHRA, NHS/WHO ICD-10 | Licence/AI reuse decision and hash |
| Public UI | Gradio aggregate-only app or static HTML | No keys, no live clinical inference |

## Design Decisions Table

| Original brief | Converged design | Reason |
|---|---|---|
| Four fixed named models | Local baseline plus versioned optional adapters | Availability and cost |
| Public 200 rows with answers | Public development metadata plus hidden test | Prevent leakage |
| NICE PDFs and BNF | Licence-cleared metadata/derived prompts; BNF excluded | Rights |
| Boolean medication safe flag | Safe/unsafe/review/insufficient information | Clinical realism |
| One overall score | Category metrics, critical misses, CIs | Avoid misleading ranking |
| Live API Space | Frozen aggregate bundle and static fallback | Privacy and reproducibility |
| Prewritten Claude winner | Neutral hypothesis policy | Research integrity |

## Impact Outcome

The strongest public contribution is an auditable answer to “where do models fail and when should
they abstain?” It gives NHS-facing teams a replayable governance template without implying safety,
NHS endorsement, regulatory approval, or clinical effectiveness.
