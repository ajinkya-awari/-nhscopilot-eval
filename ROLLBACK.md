# ROLLBACK — NHSCopilot-Eval

For the current state and the exact next gate, read `STATUS.md` before rollback work. The GitHub
repository is user-authorized and current at commit `0952d75`; benchmark publication and deployment
remain blocked.

## Documentation Rollback

1. Inspect the scoped Project 09 diff.
2. Revert only the affected control-plane batch or restore the last reviewed commit.
3. Re-run JSON, frontmatter, contamination, and rights-boundary checks.

## Dataset/Scoring Rollback

1. Stop before changing sealed labels or private manifests.
2. Preserve the failing fixture and hashes.
3. Revert the smallest authoring/scoring change and rerun contract, split, replay, and offline tests.
4. Never delete failed evidence to make a metric look clean.

## External Rollback

Provider calls, hosted artifacts, deployment, publication, and outreach require separate approval and provider-specific rollback. This control plane does not execute them.
