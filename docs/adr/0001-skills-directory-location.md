# ADR-0001: Keep Agent Skills in `.skills/` and amend the SRS wording

- Status: Accepted
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: SK-1 to SK-5, BR-3, NFR-11
- Issues: Refs #18

## Context
SRS v1.5.0 (section 6.1 and BR-3) says every skill lives at `skills/<skill-name>/SKILL.md`.
The Stage 1 repository already stores skills in `.skills/<skill-name>/SKILL.md`; `AGENTS.md`,
`scripts/validate_skills.py`, the CI workflow and the `brain-ingest` skill all use that path.
The Agent Skills format (agentskills.io) defines the content of a skill folder (a `SKILL.md`
with frontmatter), not a fixed repository location.

## Decision
`.skills/` is the canonical skills directory. The path mismatch is recorded here and the SRS
wording (section 6.1 and BR-3) is corrected in the next SRS revision. No files are moved.

## Alternatives Considered
1. Move to `skills/` as the SRS says. Rejected: touches the validator, CI, AGENTS.md and the
   existing skill for no functional gain, on the day of the Stage 2 deadline.
2. Support both paths in the validator. Rejected: two sources of truth invite drift.

## Consequences
- The SRS and the repository disagree until the SRS revision; reviewers should treat this ADR
  as the authority on the path.
- AI clients that discover skills from their own folders may need a copy or symlink step; the
  team records any such step in `docs/team-workflow.md` when it is needed.
- `scripts/validate_skills.py` keeps scanning `.skills/*/SKILL.md` unchanged.

## Brain Citations
- [[RN-08-obsidian-para-second-brain]]
