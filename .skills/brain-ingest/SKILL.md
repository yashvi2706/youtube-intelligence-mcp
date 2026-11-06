---

## 3. Agent Skill: `brain-ingest` (`.skills/brain-ingest/SKILL.md`)

Required in Stage 1 (`SK-1`) to add research notes into the Second Brain and log each run in `brain/log.md`, while citing a distilled note (`SB-3`).

### File: `.skills/brain-ingest/SKILL.md`
```markdown
---
name: brain-ingest
description: Ingest external documentation, research material, and AI session summaries into the Obsidian Second Brain vault with valid schema frontmatter, [[wikilinks]], traceability tags, and brain/log.md audit entries.
version: "1.0.0"
cited_notes:
  - "[[RN-08-obsidian-para-second-brain]]"
  - "[[RN-01-mcp-protocol-architecture]]"
---

# Skill: `brain-ingest`

## Purpose
Standardizes the ingestion of raw research material, API specifications, and AI session transcripts into the repository's Obsidian Second Brain (`brain/`). Ensures every note adheres to the PARA schema defined in `[[AGENTS]]` and `[[RN-08-obsidian-para-second-brain]]`.

## Inputs
1. `source_title`: Title of the external documentation, paper, or session.
2. `target_folder`: Destination folder (`brain/inbox/` for raw captures, or `brain/resources/` for distilled research notes).
3. `author`: Git username/name of the team member authoring the note (`SB-6`).
4. `linked_requirements`: Array of SRS requirement IDs (`FR-*`, `NFR-*`, `SK-*`).
5. `linked_issues`: Array of GitHub Issue numbers (`#1`, `#2`, etc.).
6. `raw_content`: Technical findings to summarize and link.

## Execution Procedure
1. **Validate Metadata:** Confirm `author`, `linked_requirements`, and `linked_issues` are non-empty.
2. **Generate Note Filename:** Construct a kebab-case filename prefixed with the note identifier (e.g., `RN-01-mcp-protocol-architecture.md` or `ai-session-stage1-requirements.md`).
3. **Populate Frontmatter & Body:**
   - Write YAML frontmatter containing `id`, `title`, `type`, `stage`, `author`, `created`, `requirements`, `issues`, and `prs`.
   - Synthesize the technical material into three mandatory sections:
     1. **Core Concepts & Findings**
     2. **Architectural & Requirement Impact** (linking to `FR-*`, `NFR-*`, `SK-*`)
     3. **Connected Brain Nodes** (containing at least two valid `[[wikilinks]]` to other notes and `[[index]]`).
4. **Update Index & Audit Log:**
   - Register the new note in `brain/index.md` under the appropriate PARA section.
   - Append a timestamped execution record to `brain/log.md` recording the run ID, skill name (`brain-ingest`), author, target note, and status (`SUCCESS`).
5. **Verify Integrity:** Execute `python3 scripts/validate_brain.py` to confirm zero broken `[[wikilinks]]` and valid YAML frontmatter.