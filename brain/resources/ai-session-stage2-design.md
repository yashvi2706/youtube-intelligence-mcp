---
id: AI-02
title: "AI Session Log: Stage 2 Analysis, Design Documents and Workflow Setup"
type: ai-session
stage: 2
author: "Team forkBombers"
created: "2026-11-26"
requirements: ["NFR-12", "NFR-13", "SK-2", "SK-3", "SK-4"]
issues: ["#20"]
prs: []
---

# AI Session Log: Stage 2 (Design)

## 1. Goal
Analyse the Stage 1 repository against the SRS, project statement and SDLC handout, then draft the
Stage 2 deliverables, CI and GitHub workflow for a three-member team.

## 2. Tool and inputs
Claude (Anthropic) in the chat interface. Inputs: SRS v1.5.0 PDF, project statement, SDLC handout,
the Stage 1 repository (as an archive) and a screenshot of the GitHub issue list.

## 3. What worked
- Found real defects by running the validators on a clean export of the branch rather than on the
  local working folder (empty directories, line-ending noise, missing SRS file).
- Compared SRS wording with the repository and recorded the differences as ADRs and in the
  traceability matrix instead of silently changing either side.
- Produced complete files and per-member commands; every file is read and understood by its author
  and reviewer before merge (SDLC section 6).

## 4. What failed or was limited
- The sandbox had no network, so `pytest` and `ruff` could not be installed there; the team's
  local runs and the CI result are the evidence for lint and tests.
- Content about the MCP SDK, the YouTube like timestamps and Windows token permissions could not be
  checked against live documentation; those decisions are marked Proposed.
- Drafted scoring weights, rounding granularity and API parameter ranges are proposals to confirm
  in Stage 3.

## 5. Process lesson
Local credential files were included in an archive uploaded to the AI tool. Never share the working
folder; use `git archive` or push a branch.

## Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[ai-session-stage1-requirements]], [[stage-2-review]],
  [[RN-08-obsidian-para-second-brain]]
