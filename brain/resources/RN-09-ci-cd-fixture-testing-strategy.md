---
id: RN-09
title: "Deterministic CI Fixture Testing vs. Scheduled Live API Workflows"
type: research
stage: 1
author: "Member-4"
created: "2026-11-06"
requirements: ["NFR-6", "TQ-5", "SK-4"]
issues: ["#11", "#12"]
prs: ["#103"]
---

# RN-09: Deterministic CI Fixture Testing vs. Scheduled Live API Workflows

## 1. Core Concepts & Findings
- **PR CI Workflow (`.github/workflows/ci.yml`):** Runs on every push and pull request. Must be 100% deterministic, zero-quota, and fast. Uses sanitized JSON fixtures inside `tests/fixtures/` loaded by `FixtureYouTubeDataProvider`.
- **Mandatory CI Gates (`Section 4`):**
  1. Package build & import verification
  2. Code linting (`ruff`)
  3. Automated unit/integration test suite (`pytest`)
  4. Secret scanning (regex entropy & pattern check for `AIza`, `GOCSPX-`, `ya29.`)
  5. `SKILL.md` validator (`scripts/validate_skills.py`)
  6. Second Brain schema & broken `[[wikilink]]` validator (`scripts/validate_brain.py`)

## 2. Architectural & Requirement Impact
- Directly fulfills `NFR-6` (`TQ-5`), `Section 4` CI requirements, and `SK-4` (`local-check`).

## 3. Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[RN-01-mcp-protocol-architecture]], [[RN-03-youtube-quota-budget-management]], [[RN-08-obsidian-para-second-brain]]