# Second Brain Execution Log (`brain/log.md`)

All runs of `brain-ingest`, `brain-refine`, and `brain-query` are recorded chronologically below.

| Run ID | Timestamp (UTC) | Skill Invoked | Author | Target Artifact(s) | Linked Issues / PRs | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `RUN-001` | 2026-11-06T13:51:00Z | `brain-ingest` | Yashvi | [[RN-01-mcp-protocol-architecture]] | `#6`, `#12` / `PR #102` | PASS |
| `RUN-002` | 2026-11-06T14:06:00Z | `brain-ingest` | Yashvi | [[RN-02-youtube-data-api-v3-endpoints]] | `#1`, `#2`, `#10` / `PR #102` | PASS |
| `RUN-003` | 2026-11-06T14:21:00Z | `brain-ingest` | Yashvi | [[RN-03-youtube-quota-budget-management]] | `#7`, `#12` / `PR #102` | PASS |
| `RUN-004` | 2026-11-06T14:36:00Z | `brain-ingest` | Yashvi | [[RN-04-tfidf-cosine-similarity-design]] | `#1`, `#2`, `#3` / `PR #102` | PASS |
| `RUN-005` | 2026-11-06T14:51:00Z | `brain-ingest` | Dhyan | [[RN-08-obsidian-para-second-brain]] | — | PASS |
| `RUN-006` | 2026-11-06T15:06:00Z | `brain-ingest` | Dhyan | [[RN-09-ci-cd-fixture-testing-strategy]] | — | PASS |
| `RUN-007` | 2026-11-06T15:21:00Z | `brain-ingest` | Dhyan | [[RN-10-prompt-injection-mitigation]] | — | PASS |
| `RUN-008` | 2026-11-26 | `brain-ingest` | Dhyan | [[RN-11-quota-ledger-and-cache-storage-design]] | `#7` / see [[stage-2-deliverables]] | PASS |
| `RUN-009` | 2026-11-26 | `brain-ingest` | Raj | [[RN-12-confirmation-token-design]] | `#5`, `#9` / see [[stage-2-deliverables]] | PASS |
| `RUN-010` | 2026-11-26 | `brain-ingest` | Yashvi | [[RN-13-fixture-recording-and-sanitization]] | `#11` / see [[stage-2-deliverables]] | PASS |

Notes:
- RUN-008 to RUN-010 were drafted in an AI-assisted session ([[ai-session-stage2-design]]) and
  reviewed by their authors; status PASS means `scripts/validate_brain.py` exited 0.
- Runs of `brain-refine` and `brain-query` that change the vault are appended here when they are
  executed on a branch that is merged. Scratch evaluation runs (TQ-7) are recorded only in
  `docs/testing/skill-evals.md`.
