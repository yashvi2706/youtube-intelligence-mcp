# Requirements Traceability Matrix (SE-5)

Chain: requirement -> GitHub issue -> design -> ADR -> planned code -> planned tests -> skill ->
brain note. PR numbers are recorded in `brain/projects/stage-2-deliverables.md` (branch to PR
table) so that this file does not change after merging.

Notes on numbering:
- Issue numbers are the **actual** numbers on GitHub (#1 to #12 exist). The SRS section 6.3 used
  planned numbers (#1 to #23, PRs #101 to #107); SRS TBD-1 requires the replacement. Where the
  SRS planned a different number (for example NFR-7 as #12), this table follows GitHub.
- A dash means no issue exists yet; open one at the start of Stage 3.
- "Code" and "Tests" are Stage 3 plans, not completed work.

## 1. Functional requirements
| Req | Issue | Design (`docs/architecture.md`) | ADR | Code (planned) | Tests (planned) | Skill | Brain notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FR-1 | #1 | sec 9.1, 14 | 0006 | `tools/find_similar_videos.py`, `intelligence/similarity.py` | TQ-1, 2, 3, 4, 6 | video-to-playlist | RN-02, RN-04 |
| FR-2 | #2 | sec 14 | 0006 | `tools/find_similar_channels.py`, `intelligence/similarity.py` | TQ-1, 2, 3, 4, 6 | - | RN-02, RN-04 |
| FR-3 | #3 | sec 14 | 0006 | `tools/recommend_videos.py`, `intelligence/recommend.py` | TQ-1, 2, 3, 4, 6 | - | RN-03, RN-04, RN-05 |
| FR-4 | #4 | sec 14 | 0011 | `tools/analyze_engagement.py`, `intelligence/engagement.py` | TQ-1, 2, 3, 4, 6 | - | RN-02, RN-06 |
| FR-5 | #5 | sec 9.2, 10 | 0007, 0008 | `tools/propose_playlist.py`, `tools/confirm_create_playlist.py`, `intelligence/playlist.py` | TQ-1, 2, 3, 4, 6, SEC-4 | video-to-playlist | RN-07, RN-10, RN-12 |
| REQ-1.7 / 1.8 | - | sec 8 | 0009 | `tools/get_video_details.py`, `resources.py` | TQ-1, 4 | video-to-playlist | RN-02 |
| REQ-2.6 | - | sec 8 | 0009 | `resources.py` | TQ-1, 4 | - | RN-02 |
| REQ-5.5 | - | sec 8 | - | `tools/analyze_playlist.py` | TQ-1, 3 | video-to-playlist | RN-06, RN-07 |

## 2. Nonfunctional, safety and governance requirements
| Req | Issue | Design | ADR | Code (planned) | Tests (planned) | Skill | Brain notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| NFR-1 | #6 | sec 4, 6, 7 | 0002 | `providers/` | TQ-2, 5 | local-check | RN-01, RN-09 |
| NFR-2 / SAF-1 | #7 | sec 8, 11 | 0004, 0005 | `services/quota.py` | TQ-1, 6 | - | RN-03, RN-11 |
| NFR-3 | #8 | sec 9.3, 12 | 0010 | `services/auth.py` | TQ-4, SEC-1 | - | RN-05 |
| NFR-4 | #9 | sec 4, 6 | 0009, 0008 | `sanitize.py` | TQ-4, SEC-4 | video-to-playlist | RN-10, RN-12 |
| NFR-5 | #10 | sec 13 | 0002 | `errors.py` | TQ-4, TQ-8 | - | RN-02 |
| NFR-6 | #11 | sec 2 | 0002 | `.github/workflows/` | TQ-5, TQ-7 | local-check | RN-09, RN-13 |
| NFR-7 | - | sec 12 | 0010 | `.gitignore`, CI secret scan | SEC-2, SEC-5 | - | RN-05, RN-13 |
| NFR-8 | - | sec 14 | 0006, 0007 | `intelligence/` | TQ-1 (benchmark) | - | RN-04 |
| NFR-9 | - | sec 4 | 0009 | `validation.py` | TQ-4, SEC-3 | - | RN-10 |
| NFR-10 | - | sec 4, 11 | 0002, 0005 | `services/cache.py`, `providers/cached.py` | TQ-2, 6 | - | RN-03, RN-11 |
| NFR-11 | #11 | sec 3 | 0001 | `.github/workflows/ci.yml`, `scripts/validate_*.py` | every PR | local-check | RN-09 |
| NFR-12 | - | all docs | all | `docs/` | review | - | RN-01 |
| NFR-13 | #12 | - | 0001 | `AGENTS.md`, `docs/team-workflow.md` | PR review | brain-ingest | RN-08 |
| SAF-2 / SAF-3 | #5 | sec 9.2, 10 | 0008 | `services/confirmation.py` | TQ-3, SEC-4 | video-to-playlist | RN-10, RN-12 |

## 3. Agent skills
| Req | Issue | Skill file | ADR | Tests / evals | Brain notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SK-1 | #12 | `.skills/brain-ingest/SKILL.md` | 0001 | TQ-7, `validate_skills.py` | RN-08 |
| SK-2 | - | `.skills/brain-refine/SKILL.md` | 0001 | TQ-7, `validate_skills.py` | RN-08 |
| SK-3 | - | `.skills/brain-query/SKILL.md` | 0001 | TQ-7, `validate_skills.py` | RN-08 |
| SK-4 | - | `.skills/local-check/SKILL.md`, `scripts/local_check.py` | 0001 | `tests/test_local_check.py`, TQ-7 | RN-01, RN-09, RN-13 |
| SK-5 | - | `.skills/video-to-playlist/SKILL.md` (Stage 3) | 0001 | TQ-3, TQ-7 | RN-04, RN-07, RN-10 |

## 4. Stage 1 provenance (from git history)
| Item | Author (commit) | Merged via | Note |
| :--- | :--- | :--- | :--- |
| RN-01 to RN-04 | Yashvi | PR #2 | brain-ingest runs RUN-001 to RUN-004 |
| RN-05 to RN-07 | Raj ("Add files via upload") | PR #14 | no brain-ingest runs logged for these three notes |
| RN-08 to RN-10, ai-session | Dhyan | PR #15 | RUN-005 to RUN-007 |
| Skeleton, CI, AGENTS.md | Dhyan (`bfe7aac`) | branch `feat/stage1-skeleton-and-ci` | verify the PR number on GitHub |
| SRS review notes, stage review | team | PR #16 (`stage1-srs-and-review`) | |
| Empty PARA folders restored, CI green | Yashvi | PR #17 (`fix/missing-para-dirs`) | |
Planned PR numbers (#101 to #107) in the SRS and in some Stage 1 brain notes do not exist; they
are replaced as SRS TBD-1 requires in the next SRS revision.
