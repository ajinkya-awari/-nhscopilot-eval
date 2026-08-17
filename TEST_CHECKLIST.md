# TEST CHECKLIST — NHSCopilot-Eval

## Current state — 2026-08-18

Static/offline and public-disclosure checks are evidenced. The Python test suite is authored but
has not been run locally. The next test task is the Kaggle/Colab contract command in
`nhscopilot-eval/docs/KAGGLE_COLAB_TEST_RUN.md`; unchecked items below remain gates, not failures.

## Control Plane

- [ ] `AGENTS.md` and `CLAUDE.md` name only Project 09 and agree on gates.
- [x] `.claude/settings.json` parses as JSON.
- [x] Six agents contain complete frontmatter.
- [x] Fifteen prompts mention NHSCopilot-Eval and no unrelated project terms.
- [x] No secret-like values, fabricated metrics, or stale freeze text remain in the active source boundary.

## Source Gates

- [ ] Contracts reject unknown fields, empty prompts, invalid categories, missing rights, and unstable IDs.
- [x] Exactly 200 synthetic rows are present locally: 100 guidance, 50 ICD-10, 50 medication safety.
- [ ] Rights/source manifest contains URL, version/date, licence decision, hash, and citation anchor.
- [ ] Public, private, and sealed splits are disjoint.
- [x] PHI and restricted-content scans pass for the generated public projection.
- [ ] Local baseline runs offline without provider credentials.
- [ ] Refusal, timeout, malformed, provider error, abstention, insufficient-information, and `not_run` remain distinct.
- [ ] Paired bootstrap intervals reproduce from locked rows.
- [x] Offline catalogue app reads frozen aggregates and performs no network inference by design.

## Evidence

Record command, date, environment, result, and artifact path. Never convert an unchecked box into a claim.
