---
name: brain-refine
description: Refine the Obsidian PARA second brain - move unsorted notes from brain/inbox/ into projects, areas, resources or archive, merge duplicate notes, repair broken wikilinks and frontmatter, update brain/index.md, and log the run in brain/log.md. Use after several ingests or before a stage submission.
version: "1.0.0"
cited_notes:
  - "[[RN-08-obsidian-para-second-brain]]"
  - "[[RN-01-mcp-protocol-architecture]]"
---

# Skill: `brain-refine`

## Purpose
Keeps the vault (`brain/`) organised and consistent after new material has been added (SK-2,
SB-1, SB-5). It changes structure and links, never the meaning of a note.

## Inputs
1. `scope`: `inbox` (default) or `all` notes in the vault.
2. `author`: Git name of the team member running the skill (`SB-6`).
3. `linked_issues`: GitHub issue numbers for the run (non-empty).

## Execution Procedure
1. **Baseline:** run `python scripts/validate_brain.py` and save the output; this lists the
   current schema and broken-link problems.
2. **Classify inbox notes:** for each file in `brain/inbox/` decide the PARA folder:
   `projects/` (has a deadline or stage deliverable), `areas/` (ongoing responsibility),
   `resources/` (reference or research), `archive/` (inactive). Move the file; keep the filename.
3. **Detect duplicates:** compare titles, ids and requirement lists. For a duplicate pair, keep
   the note with the earlier `created` date, merge unique content into it, and replace the other
   with a pointer only after a human confirms in the PR; never delete without confirmation.
4. **Repair frontmatter:** ensure keys `id`, `title`, `type`, `stage`, `author`, `created`,
   `requirements`, `issues`, `prs` exist (schema in `AGENTS.md`). Do not invent values; ask the
   author for missing ones.
5. **Repair links:** fix broken `[[wikilinks]]` to existing note filenames (no `.md`); add a link
   to `[[index]]` where a note has none.
6. **Update `brain/index.md`:** every note is listed under its PARA section.
7. **Log the run:** append a row to `brain/log.md` (run ID, UTC time, `brain-refine`, author,
   notes touched, issues/PRs, PASS or FAIL).
8. **Verify:** run `python scripts/validate_brain.py` again; it must exit 0.
9. **Deliver:** commit on a branch and open a PR (SB-5); a human reviews every change.

## Output
A short report: files moved, duplicates found, links repaired, items needing a human decision,
and the validator result before and after.

## Safety Rules
- Never edit the body meaning of a note; only structure, frontmatter and links.
- Never delete a note without human confirmation in the PR.
- Never write secrets or personal data into notes.
