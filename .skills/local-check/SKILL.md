---
name: local-check
description: Verify that the project works on a team member's machine in five steps - build, run the automated tests, start the local MCP server, invoke one read-only fetch tool, and report pass or fail for each step. Use before opening a PR, after pulling main, and during live reviews.
version: "0.1.0"
cited_notes:
  - "[[RN-01-mcp-protocol-architecture]]"
  - "[[RN-09-ci-cd-fixture-testing-strategy]]"
  - "[[RN-13-fixture-recording-and-sanitization]]"
---

# Skill: `local-check`

## Purpose
Gives every team member the same fast answer to "does the project work on my machine?" (SK-4,
SDLC section 3). It always runs in **fixture mode**: no network, no quota, no credentials.

## Inputs
None required. Optional flags of the driver: `--skip-build`, `--skip-tests`.
Run from the repository root with the project's virtual environment active.

## Execution Procedure
1. **Build:** `python scripts/local_check.py` runs `pip install -e ".[dev]"` (step 1).
2. **Automated tests:** the driver runs `pytest -q` with `YOUTUBE_PROVIDER_MODE=fixture` (step 2).
3. **Start local server:** if the module `youtube_mcp.server` exists, start it over stdio in fixture
   mode and confirm it stays up for 3 seconds (step 3).
4. **Read-only fetch:** call one read-only tool (`get_video_details` on a fixture video) through an
   MCP session and check that a sanitized payload comes back (step 4).
5. **Report:** print a five-row table with PASS, FAIL or SKIP per step and an overall line (step 5).

## Version 0.1 limits (Stage 2)
The server and the MCP client call do not exist until Stage 3, so steps 3 and 4 report **SKIP** and
the overall result is **INCOMPLETE**, never PASS. Stage 3 replaces the SKIPs with real checks and
raises the version to 1.0.0 (see `docs/dev-plan.md`).

## Output
A table such as:

| # | Step | Result |
| :--- | :--- | :--- |
| 1 | Build project | PASS |
| 2 | Run automated tests | PASS |
| 3 | Start local MCP server | SKIP |
| 4 | Invoke one read-only fetch tool | SKIP |
| 5 | Overall | INCOMPLETE |

Exit code 1 if any step FAILS, otherwise 0.

## Safety Rules
- Never reads or prints `.env`, `client_secret*.json` or token files.
- Never makes a live YouTube API call; use the scheduled live workflow for that (NFR-6).
- Record results of a live run in `docs/testing/skill-evals.md` (TQ-7).
