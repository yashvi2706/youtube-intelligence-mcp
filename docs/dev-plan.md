# Development Plan and Task Breakdown (SE-4)

Status: draft written at the end of Stage 2; re-confirmed at the start of Stage 3. Stage 3 and
Stage 4 deadlines are not recorded in the repository and must be added by the team in section 6.
Requirement IDs refer to SRS v1.5.0; design references are in `docs/architecture.md`.

## 1. Stage 3 goals (Testing and CI)
Implement FR-1 to FR-5 and the supporting layers behind the designed interfaces; build the test
suites TQ-1 to TQ-6; add the scheduled live-API workflow (TBD-2); deliver the `video-to-playlist`
skill (SK-5) and `local-check` v1.0; keep a defect log with regression tests (TQ-8); evaluate
skills before submission (TQ-7); write the Stage 3 review note (SB-2).

## 2. Work packages and owners (Proposed)
| WP | Scope | Files (planned) | Owner | Reviewer | Depends on |
| :--- | :--- | :--- | :--- | :--- | :--- |
| WP3.0 | Spike: MCP SDK, confirmation mechanism, Windows token permissions, like timestamps | ADR-0003, 0008, 0010, 0011 updates | all three, one each | another member | none |
| WP3.1 | Contracts and validation | `models.py`, `errors.py`, `config.py`, `validation.py`, `sanitize.py` | Raj | Yashvi | WP3.0 |
| WP3.2 | Providers, storage, quota, cache | `providers/{fixture,metered,cached,live}.py`, `storage.py`, `services/{quota,cache}.py`, `tests/fixtures/` | Yashvi | Dhyan | WP3.1 |
| WP3.3 | Intelligence | `intelligence/{text,similarity,recommend,engagement,playlist}.py` | Dhyan | Raj | WP3.1 |
| WP3.4 | MCP surface | `server.py`, `tools/*.py`, `resources.py`, `services/{confirmation,auth}.py` | Raj | Yashvi | WP3.2, WP3.3 |
| WP3.5 | Skill and CI | `.skills/video-to-playlist/SKILL.md`, `local-check` v1.0, `.github/workflows/live-api-tests.yml` | Dhyan (skill), Yashvi (local-check, live workflow) | Raj | WP3.4 |
| WP3.6 | Tests and defects | `tests/{unit,integration,system,negative,security}/`, `docs/testing/` | each owner for own modules | cross-review | WP3.2 to WP3.4 |
| WP3.7 | Close-out | review note, skill evals, index/log, traceability update | rotating | rotating | all |

Each work package is one or more branches with the naming in `docs/team-workflow.md`; every PR
needs an approval from a different member.

## 3. Test plan by requirement (TQ-1 to TQ-8)
| TQ | Scope | Planned location | Key cases |
| :--- | :--- | :--- | :--- |
| TQ-1 | Unit | `tests/unit/` | similarity scoring, ISO 8601 duration parsing, playlist constraint selection, estimator table, sanitizer, validation, tool handlers, 500 ms benchmark (NFR-8) |
| TQ-2 | Integration | `tests/integration/` | tool + provider stack + cache + ledger with the fixture provider; cache hit costs 0 units and returns under 20 ms |
| TQ-3 | System | `tests/system/` | FR-1 to FR-5 end to end through the MCP interface; no tool can modify or delete playlists; created playlists are private |
| TQ-4 | Negative | `tests/negative/` | catalogue below |
| TQ-5 | Fixture CI vs live | `.github/workflows/ci.yml`, `live-api-tests.yml` | PR runs offline; live workflow scheduled, at most 500 units per run |
| TQ-6 | Quota refusal | `tests/unit/`, `tests/integration/` | over-budget request rejected before any provider call |
| TQ-7 | Skill evals | `docs/testing/skill-evals.md` | results recorded before each stage submission |
| TQ-8 | Regression | with each defect | every significant defect gets a named regression test |

### 3.1 Negative-test catalogue (TQ-4, issue #10)
| Case | Input | Expected |
| :--- | :--- | :--- |
| Malformed video ID / URL | `abc`, 12-character ID, bad URL | `INVALID_VIDEO_ID`, zero provider calls |
| Legacy channel URL | `/c/name`, `/user/name` | `INVALID_IDENTIFIER`, zero provider calls |
| Private or deleted video | ID absent from `videos.list` | `VIDEO_NOT_FOUND_OR_PRIVATE` |
| Missing tags / topics / duration | fixture without tags, live stream | weights re-normalised, flag in output |
| `quotaExceeded` from YouTube | error fixture | `QUOTA_EXCEEDED`, ledger marked exhausted |
| Budget too low | estimate above remaining | `QUOTA_BUDGET_EXCEEDED`, zero calls |
| `youtubeSignupRequired` | error fixture on `playlists.insert` | `YOUTUBE_CHANNEL_REQUIRED`, nothing written |
| Expired / revoked token | `invalid_grant` fixture | `REAUTH_REQUIRED` |
| HTTP 429 persistent | 4 consecutive 429 | `RATE_LIMITED` after 3 retries with backoff 1 s, 2 s, 4 s |
| HTTP 5xx persistent | 4 consecutive 503 | `UPSTREAM_UNAVAILABLE` |
| Failure part-way through creation | insert fails on item k | `PLAYLIST_PARTIALLY_CREATED` with inserted and missing IDs |
| Out-of-range parameters | `limit=0`, `limit=26`, `window_days=6` | `INVALID_PARAMETER` |
| Unknown field | extra property | `INVALID_PARAMETER` |
| Confirmation abuse | wrong token, reused token, expired token, no consent | `PROPOSAL_INVALID_OR_EXPIRED` or `CONFIRMATION_REQUIRED` |
| Prompt injection | hostile title/description/tags | no write, text treated as data (SEC-4) |

## 4. Stage 4 goals (Review)
Live demonstration of FR-1 to FR-5 in the MCP client, `video-to-playlist` end to end, `local-check`
live, `brain-query` live, and a walkthrough from a brain note to an ADR, code and a test; final
documentation (`README.md`, `docs/user-guide.md`, final `docs/api-reference.md`), `CHANGELOG.md`,
and the final release tag.
| WP | Scope | Owner (Proposed) |
| :--- | :--- | :--- |
| WP4.1 | README, user guide, example prompts | Yashvi |
| WP4.2 | Final API reference and architecture update | Dhyan |
| WP4.3 | Demo script, rehearsal, live-run checklist | Raj |
| WP4.4 | Changelog, release tag, final traceability | rotating |

## 5. Risks
| Risk | Mitigation |
| :--- | :--- |
| Client lacks a user-confirmation feature (DEP-2) | WP3.0 spike; tool approval dialog fallback (ADR-0008) |
| Daily quota exhausted during live tests | fixtures for CI; live workflow capped at 500 units; one project only |
| OAuth refresh token expires after 7 days (Testing mode) | re-authorisation flow; re-sign-in before demos (ADR-0010) |
| Merge conflicts on shared brain files | only the stage close-out PR edits `index.md` and `log.md` |
| Windows token-file permissions | verify in WP3.0, document in ADR-0010 |

## 6. Dates (to be filled by the team)
| Milestone | Date |
| :--- | :--- |
| Stage 3 deadline | |
| Stage 4 live review | |
