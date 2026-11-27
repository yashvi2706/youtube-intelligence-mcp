---
id: PROJ-02
title: "Stage 2 Deliverables Tracker and Traceability Baseline"
type: project
stage: 2
author: "Raj Gandhi (rajg2906)"
created: "2026-11-26"
requirements: ["NFR-12", "NFR-13", "SK-2", "SK-3", "SK-4", "NFR-1", "NFR-2", "NFR-3", "NFR-4"]
issues: ["#18", "#19", "#20"]
prs: []
---

# Stage 2 Deliverables Tracker

Stage 2 (Design) deliverables from the SDLC handout: architecture and design documentation with
diagrams, the `brain-refine` and `brain-query` skills, and the first version of `local-check`.
SRS anchors: SE-2, SE-3, SE-4, SE-5, SK-2, SK-3, SK-4, NFR-12.

## Stage 2 Checklist
- [ ] Architecture and design document with UML/ER diagrams: `docs/architecture.md` (SE-2).
- [ ] ADRs `docs/adr/0001` to `0011`, each citing a brain note (SE-3, SB-3), validated by CI.
- [ ] `brain-refine` and `brain-query` skills in `.skills/` (SK-2, SK-3).
- [ ] `local-check` skill v0.1 with driver `scripts/local_check.py` and tests (SK-4).
- [ ] Developer API design contract: `docs/api-reference.md` (SE-7, draft).
- [ ] Development plan and task breakdown: `docs/dev-plan.md` (SE-4).
- [ ] Traceability matrix: `docs/traceability.md` (SE-5).
- [ ] Governance: ADR and placeholder CI gates, completed `AGENTS.md`, workflow doc, SRS in repo.
- [ ] New brain notes by all three members: [[RN-11-quota-ledger-and-cache-storage-design]],
  [[RN-12-confirmation-token-design]], [[RN-13-fixture-recording-and-sanitization]] (SB-6).
- [ ] Skill evaluations executed and recorded in `docs/testing/skill-evals.md` (TQ-7).
- [ ] Review note [[stage-2-review]] completed by all three members (SB-2).
- [ ] AI session logged: [[ai-session-stage2-design]] (BR-4).

## Branch to Pull Request Log
Pre-Stage 2 fixes already merged: PR #16 (`stage1-srs-and-review`) and PR #17
(`fix/missing-para-dirs`, empty PARA folders, CI green).

| Branch | Author | Reviewer | Merge order | PR |
| :--- | :--- | :--- | :--- | :--- |
| `docs/stage2-governance-and-local-check` (governance, CI gates, local-check, traceability) | Yashvi | Dhyan | 1st | #21 |
| `docs/stage2-design-and-skills` (architecture, API contract, brain skills, plan) | Dhyan | Raj | 2nd | #22 |
| `docs/stage2-adrs-and-closeout` (ADRs, index/log, review, evals) | Raj | Yashvi | 3rd | #23 |

## Open Items Carried to Stage 3
ADR-0003 (MCP SDK), ADR-0008 (user-consent mechanism) and ADR-0011 (like timestamps) are
Proposed and need spikes; Windows token-file protection (ADR-0010); issues for SK-2 to SK-5 and
the remaining NFRs; SRS revision for the `.skills/` path and real issue/PR numbers (TBD-1).

## Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[stage-2-review]], [[stage-1-deliverables]], [[ai-session-stage2-design]],
  [[RN-08-obsidian-para-second-brain]]
