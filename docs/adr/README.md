# Architecture Decision Records

ADRs record significant design decisions (SE-3). Each cites at least one distilled brain note
(SB-3). `scripts/validate_adrs.py` checks the format in CI.

## Template
```markdown
# ADR-NNNN: Short decision title

- Status: Proposed | Accepted | Deprecated | Superseded
- Date: YYYY-MM-DD
- Deciders: names
- Requirements: FR-x, NFR-y
- Issues: Refs #n

## Context
## Decision
## Alternatives Considered
## Consequences
## Brain Citations
- [[RN-xx-note-name]]
```
File name: `NNNN-kebab-case-title.md`, numbers never reused. To change a decision, add a new ADR
and mark the old one `Superseded`.

## Index
| ADR | Title | Status | Requirements |
| :--- | :--- | :--- | :--- |
| [0001](0001-skills-directory-location.md) | Keep Agent Skills in `.skills/` | Accepted | SK-1..5, BR-3 |
| [0002](0002-provider-interface-and-decorators.md) | Provider interface, fixture provider and decorators | Accepted | NFR-1, SE-6, TQ-5 |
| [0003](0003-mcp-sdk-and-transport.md) | MCP SDK and stdio transport | Proposed | NFR-11, DEP-2 |
| [0004](0004-preflight-quota-estimation.md) | Pre-flight quota estimation and reservation | Accepted | NFR-2, SAF-1, TQ-6 |
| [0005](0005-local-state-storage-sqlite.md) | Local state in SQLite (WAL) | Accepted | NFR-2, NFR-10, REQ-5.3 |
| [0006](0006-similarity-scoring-design.md) | Similarity scoring design | Accepted | FR-1, FR-2, REQ-1.3, REQ-2.2 |
| [0007](0007-playlist-selection-algorithm.md) | Playlist selection (bounded knapsack) | Accepted | FR-5, REQ-5.2 |
| [0008](0008-confirmation-token-and-user-consent.md) | Confirmation token and user consent | Proposed | REQ-5.3, REQ-5.4, SAF-3 |
| [0009](0009-untrusted-metadata-sanitization.md) | Untrusted metadata sanitization | Accepted | NFR-4, SEC-4 |
| [0010](0010-oauth-credentials-and-reauthorization.md) | OAuth credential storage and re-authorisation | Accepted | NFR-3, NFR-7, SEC-1 |
| [0011](0011-activity-timestamp-source.md) | Activity timestamp source for engagement analysis | Proposed | REQ-4.2, TBD-3 |

"Proposed" means the decision depends on a Stage 3 spike or a fact that must be verified against
the live API; it becomes "Accepted" through a PR that records the result.
