# TEST CHECKLIST — NHSCopilot-Eval

## Control Plane

- [ ] `AGENTS.md` and `CLAUDE.md` name only Project 09 and agree on gates.
- [ ] `.claude/settings.json` parses as JSON.
- [ ] Six agents contain complete frontmatter.
- [ ] Fifteen prompts mention NHSCopilot-Eval and no unrelated project terms.
- [ ] No secret-like values, fabricated metrics, or stale freeze text remain.

## Source Gates

- [ ] Contracts reject unknown fields, empty prompts, invalid categories, missing rights, and unstable IDs.
- [ ] Exactly 200 rows are present: 100 guidance, 50 ICD-10, 50 medication safety.
- [ ] Rights/source manifest contains URL, version/date, licence decision, hash, and citation anchor.
- [ ] Public, private, and sealed splits are disjoint.
- [ ] PHI and restricted-content scans pass.
- [ ] Local baseline runs offline without provider credentials.
- [ ] Refusal, timeout, malformed, provider error, abstention, insufficient-information, and `not_run` remain distinct.
- [ ] Paired bootstrap intervals reproduce from locked rows.
- [ ] Offline catalogue app reads frozen aggregates and performs no network inference.

## Evidence

Record command, date, environment, result, and artifact path. Never convert an unchecked box into a claim.
