---
id: REV-02
title: "Stage 2 Retrospective & Review Note (SB-2)"
type: review
stage: 2
author: "Team forkBombers"
created: "2026-11-26"
requirements: ["NFR-12", "NFR-13", "SK-2", "SK-3", "SK-4"]
issues: ["#20"]
prs: []
---

# Stage 2 Review Note (`SB-2`)

## 1. What Worked
- Analysing the Stage 1 repository before building anything exposed problems early: a clean
  checkout fails the brain validator because empty `brain/inbox/` and `brain/archive/` folders are
  not tracked by Git (fixed in PR #17, which made CI green again), the SRS was missing from the
  repository, and the CI workflow targeted a branch that does not exist. The SRS file and the
  governance documents were added in the Stage 2 governance PR.
- Writing the design and ADRs against the SRS surfaced open decisions that code would have hidden:
  the `.skills/` versus `skills/` path (ADR-0001), the user-consent mechanism for playlist writes
  (ADR-0008) and the source of like timestamps (ADR-0011).
- Yashvi: validating a clean export of the branch exposed the missing empty PARA folders before submission; PR #17 fixed it and CI went green.
- Dhyan: the design branch passed ruff, all validators and the tests locally before the PR was opened, so review could focus on content.
- Raj: the placeholder gate in CI stopped the close-out PR from merging with unfilled results, which forced real PR numbers and evaluation results to be recorded.

## 2. What Did Not Work
- Stage 1 notes cite planned PR numbers (#101 to #104) that do not exist, and three research notes
  (RN-05 to RN-07) were added by file upload without a logged `brain-ingest` run.
- A zip of the working folder, including local credential files, was shared with an AI tool.
  Repository content must be shared with `git archive` or a pushed branch only (SDLC section 6).
- The AI sandbox used for drafting could not install `pytest` or `ruff`, so lint and tests were
  only proven by the team's own runs and by CI.
- Windows `Zone.Identifier` files were committed from a copied zip and blocked pulls on Windows until they were removed; a command block meant for another member was run by mistake; and code copied from chat lost its double underscores, breaking one test until the file was restored. Share files with `git archive`, extract zips inside the repo environment, and copy code with the copy button.

## 3. What to Change for Stage 3
- Start Stage 3 with the spike tasks (WP3.0 in `docs/dev-plan.md`) and update ADR-0003, ADR-0008,
  ADR-0010 and ADR-0011 with the observed results.
- Open GitHub issues for SK-2 to SK-5 and the remaining NFRs, and keep issue and PR numbers in the
  traceability matrix exact.
- Record fixtures only through the scrub procedure in [[RN-13-fixture-recording-and-sanitization]].
- Run each skill before submission and record results in `docs/testing/skill-evals.md` (TQ-7).

## Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[stage-2-deliverables]], [[stage-1-review]], [[ai-session-stage2-design]],
  [[RN-08-obsidian-para-second-brain]]
