# Skill Evaluations (TQ-7)

Every active Agent Skill is evaluated before each stage submission and the result is recorded
here. This file is the protocol and the Stage 2 result log. A result is written only after the
evaluation was actually run; nothing is pre-filled.

## 1. How to run an evaluation
1. Use a clean checkout of the branch under test (`git archive` export or fresh clone).
2. Open the repository in the AI client (Claude Code or equivalent) so the skill in `.skills/`
   is available; give exactly the prompt in the table below.
3. Check every pass criterion. Record date, runner, result and a one-line note.
4. For a FAIL, open a GitHub issue and add a regression case (TQ-8).

## 2. Automated checks (all skills)
| Command | Expected | Date | Run by | Result |
| :--- | :--- | :--- | :--- | :--- |
| `python scripts/validate_skills.py` | `SUCCESS: Validated 4 skill(s)` | <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> |
| `python scripts/validate_brain.py` | `SUCCESS` and note counts | <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> |
| `python scripts/validate_adrs.py` | `SUCCESS: Validated 11 ADR(s)` | <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> |
| `pytest -v` (fixture mode) | all tests pass | <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> |

## 3. Skill evaluations
### 3.1 `brain-ingest` (SK-1)
- Prompt: "Use brain-ingest to add a note summarising the MCP Inspector tool (author: <name>, issue #1)."
- Pass criteria: new note under `brain/resources/` with valid frontmatter and at least two
  wikilinks plus `[[index]]`; `brain/index.md` updated; `brain/log.md` row appended;
  `validate_brain.py` exits 0.
| Date | Run by | Result | Notes |
| :--- | :--- | :--- | :--- |
| <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> |

### 3.2 `brain-refine` (SK-2)
- Setup: place a copy of any valid note in `brain/inbox/`.
- Prompt: "Use brain-refine with scope inbox, author <name>, linked issue #1."
- Pass criteria: the note moves to the correct PARA folder; index updated; log row appended;
  validator exits 0; no note body text changed; nothing deleted without a prompt.
| Date | Run by | Result | Notes |
| :--- | :--- | :--- | :--- |
| <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> |

### 3.3 `brain-query` (SK-3)
- Prompt: "Use brain-query: which notes cover similarity scoring, and which requirements do they support?"
- Pass criteria: starts from `brain/index.md`; cites `[[RN-04-tfidf-cosine-similarity-design]]` and
  related notes by link; names FR-1, FR-2 and NFR-8; states any gap instead of inventing facts.
| Date | Run by | Result | Notes |
| :--- | :--- | :--- | :--- |
| <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> |

### 3.4 `local-check` v0.1 (SK-4)
- Command: `python scripts/local_check.py`
- Pass criteria in Stage 2: step 1 PASS, step 2 PASS, steps 3 and 4 SKIP with the reasons shown,
  overall `INCOMPLETE`, exit code 0; no step is reported PASS without running.
| Date | Run by | Result | Notes |
| :--- | :--- | :--- | :--- |
| <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> | <TEAM-FILL> |

### 3.5 `video-to-playlist` (SK-5)
Not yet implemented (Stage 3). Evaluation cases are added in the Stage 3 branch.
