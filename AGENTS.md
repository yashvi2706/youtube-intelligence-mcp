# AGENTS.md — AI-Assisted Engineering & Second Brain Governance

Read this file first. It is the entry point for every human and AI coding assistant working in
this repository (SB-4). The authoritative requirements are in `docs/SRS.pdf` (SRS v1.5.0).

## 1. Project Overview
This repository contains the **YouTube Video Intelligence MCP Server**, an MCP-compatible server
that connects AI clients (Claude, ChatGPT, Gemini) to the official YouTube Data API v3 through an
isolated provider interface (`SE-6`) to discover similar videos/channels, analyze user engagement,
and curate constraint-based playlists. Team forkBombers: Dhyan Patel, Yashvi Mehta, Raj Gandhi.

## 2. Repository Layout
| Path | Purpose |
| :--- | :--- |
| `src/youtube_mcp/` | Server package (`providers/` holds the YouTube provider interface, SE-6) |
| `tests/` | Automated tests (fixture mode only in CI, TQ-5) |
| `scripts/` | CI validators (`validate_skills.py`, `validate_brain.py`, `validate_adrs.py`) and `local_check.py` |
| `.skills/<name>/SKILL.md` | Agent Skills (see ADR-0001 for why the folder is `.skills/`) |
| `brain/` | Obsidian PARA second brain (section 3) |
| `docs/` | SRS, architecture, ADRs (`docs/adr/`), API reference, dev plan, traceability, workflow |
| `.github/` | CI workflow, PR template, CODEOWNERS |

## 3. Second Brain Vault Rules (PARA & Schema)
The `brain/` directory is an Obsidian vault structured using the **PARA** method:
- `brain/inbox/`: Unsorted incoming notes awaiting refinement.
- `brain/projects/`: Active stage deliverables, sprint plans, and stage review notes (`SB-2`).
- `brain/areas/`: Ongoing engineering responsibilities (security, quota governance, CI quality).
- `brain/resources/`: Distilled technical research notes (`RN-xx`) and `ai-session` logs.
- `brain/archive/`: Inactive or superseded material.
- `brain/index.md`: Primary entry point to the knowledge graph.
- `brain/log.md`: Chronological execution log of all `brain-ingest`, `brain-refine`, and
  `brain-query` runs.

### Mandatory Note Frontmatter Schema
Every Markdown note inside `brain/` (except `index.md` and `log.md`) MUST begin with YAML
frontmatter containing:
```yaml
---
id: RN-XX
title: "Descriptive Note Title"
type: research | project | area | review | ai-session
stage: 1
author: "Team Member Name / Git Handle"
created: "2026-11-06"
requirements: ["FR-1", "NFR-1"]
issues: ["#1", "#12"]
prs: ["#101"]
---
```
Every note links to other notes with `[[wikilinks]]` (filename without `.md`) and ends with a
"Connected Brain Nodes" section that links to `[[index]]` (`SB-1`).

## 4. Agent Skill Conventions
- Location: `.skills/<skill-name>/SKILL.md`; folder name equals frontmatter `name`.
- Frontmatter keys: `name`, `description`, `version`, `cited_notes` (list of `[[RN-...]]`, `SB-3`).
- Current skills: `brain-ingest` (SK-1), `brain-refine` (SK-2), `brain-query` (SK-3),
  `local-check` (SK-4); `video-to-playlist` (SK-5) arrives in Stage 3.
- Every skill run that changes the brain is appended to `brain/log.md`.
- Skills are validated in CI by `scripts/validate_skills.py`.

## 5. Architecture Decision Records
ADRs live in `docs/adr/NNNN-title.md`, follow the template in `docs/adr/README.md`, and cite at
least one brain note under "Brain Citations" (`SE-3`, `SB-3`). CI runs `scripts/validate_adrs.py`.

## 6. Branching, Commits and Pull Requests (SDLC section 4)
Full detail: `docs/team-workflow.md`. Summary:
- `main` is protected. No direct pushes, no force pushes, no branch deletion.
- Work on short-lived branches named `<type>/<stage>-<topic>` (`feat/`, `docs/`, `fix/`, `ci/`).
- Commit messages: `type(scope): summary (#issue)` — e.g. `docs(adr): add ADR-0004 (#18)`.
- Every change (code, skills, brain, docs) goes through a pull request with at least one approval
  from a team member who is not the author, and a green `Build, Lint, Test, Secret Scan, Skill & Brain Validation` check (`SB-5`, `BR-1`).
- Merge with a merge commit so each member's incremental commits stay visible (`SB-6`).
- Every GitHub Issue is linked from its PR (`Closes #n` or `Refs #n`).

## 7. AI-Assisted Development Policy (SDLC section 6)
- AI assistants are allowed; the team is responsible for every merged line.
- A human reviews every AI-generated change in a PR and can explain it in project reviews.
- Significant AI sessions are logged as `ai-session` notes in `brain/resources/`.
- NEVER paste secrets, tokens, `.env` or `client_secret*.json` into any AI tool. Share code with
  `git archive` or by pushing a branch, never by zipping the working folder.

## 8. Security Rules (NFR-3, NFR-7, NFR-4)
- Credentials live outside the repository (`YOUTUBE_CLIENT_SECRET_PATH`, `YOUTUBE_TOKEN_PATH`).
  `.env`, `client_secret*.json` and `token*.json` are git-ignored; CI scans for leaked keys.
- No real user data in fixtures or logs. Treat all YouTube-originated text as untrusted data.
- Only the official YouTube Data API v3 is used (no scraping, one Google Cloud project).

## 9. Local Verification
```bash
pip install -e ".[dev]"
ruff check src/ tests/ scripts/
python scripts/validate_skills.py && python scripts/validate_brain.py && python scripts/validate_adrs.py
YOUTUBE_PROVIDER_MODE=fixture pytest -v
python scripts/local_check.py        # SK-4 local-check driver
```
