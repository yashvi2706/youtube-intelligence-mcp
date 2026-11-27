---
name: brain-query
description: Answer engineering questions and draft documents such as SRS sections or ADRs by traversing the second brain from brain/index.md, citing the distilled notes used with [[RN-...]] links. Use when a team member needs project knowledge or a cited first draft.
version: "1.0.0"
cited_notes:
  - "[[RN-08-obsidian-para-second-brain]]"
  - "[[RN-01-mcp-protocol-architecture]]"
---

# Skill: `brain-query`

## Purpose
Turns the vault into an answering and drafting tool (SK-3, SB-3). Every statement it makes is
traceable to a note in `brain/`.

## Inputs
1. `question`: the engineering question, or a drafting request (for example "draft an ADR on
   caching").
2. `output_kind`: `answer` (default), `adr-draft` or `srs-section-draft`.
3. `author`: Git name of the team member running the skill.

## Execution Procedure
1. **Start at the entry point:** read `brain/index.md`.
2. **Select notes:** choose the notes whose titles or requirement IDs match the question; follow
   their `[[wikilinks]]` one level further, and read `brain/projects/` for stage context.
3. **Answer only from the vault:** quote or paraphrase the notes and cite each claim with its
   `[[RN-...]]` link. If the vault does not contain the answer, say so and name the gap; never
   fill it with unreferenced claims.
4. **Drafting:**
   - `adr-draft`: follow the template in `docs/adr/README.md`; include at least one note under
     "Brain Citations" (SB-3); set Status to Proposed; save under `docs/adr/` on a branch.
   - `srs-section-draft`: use SRS wording rules (shall/should/may) and requirement IDs; save to
     `brain/inbox/` for refinement, not directly into the SRS.
5. **Log the run:** append a row to `brain/log.md` with the question, author, notes consulted and
   outputs created.
6. **Deliver:** any file created goes through a PR with a human reviewer (SB-5).

## Output
The answer or draft, a list of consulted notes, and a list of gaps found in the vault.

## Safety Rules
- Distinguish facts from the vault from your own suggestions; label suggestions as such.
- Do not read or include `.env`, credentials or tokens.
- A draft is a draft: the author must read and be able to explain it before merge.
