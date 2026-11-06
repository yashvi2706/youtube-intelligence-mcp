---
id: RN-08
title: "Obsidian PARA Second Brain Schema & Agent Skills Format"
type: research
stage: 1
author: "Member-3"
created: "2026-11-06"
requirements: ["SK-1", "SK-2", "SK-3"]
issues: ["#12"]
prs: ["#103"]
---

# RN-08: Obsidian PARA Second Brain Schema & Agent Skills Format

## 1. Core Concepts & Findings
- **PARA Structure:** Organizes knowledge by actionability (`Projects` -> `Areas` -> `Resources` -> `Archive`) rather than arbitrary topic hierarchies, keeping active stage work separated from reference material.
- **Graph Integrity:** Obsidian resolves `[[wikilinks]]` across folders. Automated CI validation (`scripts/validate_brain.py`) ensures every `[[target]]` resolves to an existing `.md` file and every note includes traceability fields (`requirements`, `issues`, `prs`).
- **`agentskills.io` Format:** Each skill resides in `.skills/<skill-name>/SKILL.md` with YAML frontmatter validated by `scripts/validate_skills.py`.

## 2. Architectural & Requirement Impact
- Serves as the foundational distilled note cited by `SK-1` (`brain-ingest`), `SK-2` (`brain-refine`), and `SK-3` (`brain-query`) per `SB-3`.

## 3. Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[RN-01-mcp-protocol-architecture]], [[RN-09-ci-cd-fixture-testing-strategy]], [[stage-1-deliverables]]