# Team Workflow — Branching, Pull Requests, Reviews and Merges

Applies to Stages 2 to 4. Source requirements: SDLC section 4 (GitHub and Team Development),
SRS BR-1, BR-2, NFR-13, SB-5, SB-6.

## 1. People
| Role label | Name | GitHub handle |
| :--- | :--- | :--- |
| Member 1 (repository owner) | Yashvi Mehta | `yashvi2706` |
| Member 2 | Dhyan Patel | `dhyanspatel49` |
| Member 3 | Raj Gandhi | `rajg2906` |

## 2. Branch strategy
- `main` is the only long-lived branch. There is no `develop` branch.
- Feature branches are short-lived, branch from the latest `main`, and are deleted after merge.
- Name: `<type>/<stage>-<topic>` with type `feat`, `docs`, `fix` or `ci`.
- Stage 1 branches (`stage1-srs-and-review`, `fix/missing-para-dirs`, PRs #16 and #17) are merged and
  can be deleted.
- One purpose per branch. Two members never edit the same file on different branches in the
  same stage; the ownership table in section 6 is the allocation.
- Stage 2 uses exactly three branches, one pull request per member.
- `brain/index.md` and `brain/log.md` are the only shared files. They are edited in the final
  Stage PR only, to avoid merge conflicts.

## 3. Commits
- Small, meaningful commits: `type(scope): summary (#issue)`.
- Types: `feat`, `fix`, `docs`, `test`, `ci`, `chore`, `refactor`.
- Each member commits their own work under their own Git identity (SB-6, BR-2).

## 4. Pull request rules
1. Open the PR against `main` using the PR template; link the issue and requirement IDs.
2. Another member (never the author) reviews and approves; the author merges after approval.
3. The `Build, Lint, Test, Secret Scan, Skill & Brain Validation` check (workflow "Stage 1-4 CI Pipeline") must be green and all review
   conversations resolved. Never rename that job without updating the ruleset first.
4. Merge method: **merge commit** (keeps each member's incremental commits visible).
5. Delete the branch after merge, then sync local `main`.
6. AI-generated content is allowed but must be read and understood by author and reviewer.
7. If a push after approval changes the diff, the approval is dismissed and must be given again.

## 5. Review and merge rotation (Stage 2)
| Order | Branch | PR title | Author (dev) | Reviewer / approver | Merger |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `docs/stage2-governance-and-local-check` | Governance docs, ADR/placeholder CI gates, local-check v0.1, traceability | Yashvi | Dhyan | Yashvi |
| 2 | `docs/stage2-design-and-skills` | Architecture, API contract, brain-refine, brain-query, dev plan | Dhyan | Raj | Dhyan |
| 3 | `docs/stage2-adrs-and-closeout` | ADR-0002 to ADR-0011, index/log, review note, skill evals | Raj | Yashvi | Raj |

Merge order is strict: 1, then 2, then 3. Reviews do not depend on merge order, so a reviewer can
start while the next PR is still being written. PR 1 merges first because it adds the ADR
validator that PRs 2 and 3 are checked by; PR 3 merges last because `brain/index.md` links to notes
created in PRs 1 and 2. Authors of PRs 2 and 3 branch from `main` after the previous PR has merged
(or run `git merge origin/main` into their branch).

## 6. File ownership (Stage 2)
| Branch / owner | Files |
| :--- | :--- |
| `docs/stage2-governance-and-local-check` (Yashvi) | `.gitattributes`, `AGENTS.md`, `docs/SRS.pdf`, `docs/SRS.md`, `.github/CODEOWNERS`, `.github/pull_request_template.md`, `.github/workflows/ci.yml` (two added steps), `docs/team-workflow.md`, `scripts/validate_adrs.py`, `docs/adr/0001-skills-directory-location.md`, `.skills/local-check/SKILL.md`, `scripts/local_check.py`, `tests/test_local_check.py`, `docs/traceability.md`, `brain/resources/RN-13-fixture-recording-and-sanitization.md` |
| `docs/stage2-design-and-skills` (Dhyan) | `docs/architecture.md`, `docs/api-reference.md`, `docs/dev-plan.md`, `.skills/brain-refine/SKILL.md`, `.skills/brain-query/SKILL.md`, `brain/resources/RN-11-quota-ledger-and-cache-storage-design.md` |
| `docs/stage2-adrs-and-closeout` (Raj) | `docs/adr/README.md`, `docs/adr/0002` to `docs/adr/0011`, `brain/resources/RN-12-confirmation-token-design.md`, `brain/index.md`, `brain/log.md`, `brain/projects/stage-2-deliverables.md`, `brain/projects/stage-2-review.md`, `brain/resources/ai-session-stage2-design.md`, `docs/testing/skill-evals.md` |

Before Stage 2: PR #17 (Yashvi) restored the empty PARA folders and made CI green again.
Stages 3 and 4 ownership is defined in `docs/dev-plan.md`.

## 7. Handling conflicts
- Rebase is not used. Update a branch with `git merge origin/main`.
- If `brain/index.md` or `brain/log.md` conflicts, keep both sides' lines, preserve table
  column order and run `python scripts/validate_brain.py` before committing the merge.
- Never resolve a conflict in a file another member owns without asking them.

## 8. After a PR is merged
```bash
git checkout main && git pull origin main
git branch -d <merged-branch>
git fetch --prune
```

## 9. Security reminders
Never commit `.env`, `client_secret*.json`, `token*.json` or real user data. Never paste them
into an AI tool. Share code through branches or `git archive`, never by zipping the folder.
