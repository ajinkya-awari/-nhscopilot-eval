# ARCHITECTURE — NHSCopilot-Eval

| Area | Responsibility | Boundary |
|---|---|---|
| Contracts | Validate rows, manifests, registry entries, and outcomes | Reject unknown or unstable data |
| Provenance | Track URL, edition, licence, hash, and citation anchor | No rights decision, no content |
| Dataset | Author controlled synthetic/licence-cleared rows and splits | Never mix hidden labels into public bundles |
| Providers | Run local baseline and optional remote adapters | No silent substitution or unbounded calls |
| Scoring | Category metrics, abstention, safety misses, errors | No prewritten winner |
| Analysis | Paired bootstrap and aggregate tables | No raw restricted text |
| App | Display frozen aggregates and disclaimers | No live clinical inference |

The provider layer may depend on contracts and redaction utilities. The public app consumes frozen aggregates only. Tests default to synthetic fixtures and offline mode.
