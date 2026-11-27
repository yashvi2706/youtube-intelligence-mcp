---
id: RN-13
title: "Fixture Recording and Sanitization for Deterministic, Privacy-Safe Tests"
type: research
stage: 2
author: "Yashvi Mehta (yashvi2706)"
created: "2026-11-26"
requirements: ["NFR-1", "NFR-6", "NFR-7", "TQ-5", "SEC-2", "SEC-5"]
issues: ["#18", "#11"]
prs: []
---

# RN-13: Fixture Recording and Sanitization for Deterministic, Privacy-Safe Tests

## 1. Core Concepts & Findings
- CI must never call YouTube (TQ-5), so tests read recorded API responses through the fixture
  provider. A fixture is one JSON file per provider call, named by method and a stable key
  (for example video ID), stored under `tests/fixtures/`.
- Recording is a one-off, manual step run against the live API with a small quota budget (about
  500 units, NFR-6). The recorder must be separate from the test run so tests stay offline.
- Before a recording is committed it is scrubbed: user-specific lists (likes, subscriptions,
  private playlists) are replaced by synthetic data with invented IDs, and any account name,
  e-mail, channel ID of the tester or token is removed (SEC-5). Public videos used as examples
  are kept only if they hold no personal data.
- Error fixtures are written by hand from the documented API error format so each negative case
  in TQ-4 (`quotaExceeded`, `youtubeSignupRequired`, 429, 5xx, expired token) is reproducible.
- Hostile-metadata fixtures (titles or descriptions containing instruction-like text) feed the
  prompt-injection tests (SEC-4); they are invented, never copied from real accounts.
- The CI secret scan (`AIza...`, `GOCSPX-...`, `ya29....` patterns) is the backstop, not the plan:
  scrub first, then scan.

## 2. Architectural & Requirement Impact
- `FixtureProvider` (ADR-0002) loads these files; `local-check` and the CI suite depend on them
  (`docs/architecture.md` sections 4 and 7).
- A fixture checklist is added to the PR template for Stage 3: scrubbed, no real IDs of the tester,
  scan green.

## 3. Connected Brain Nodes
- Source notes: [[RN-09-ci-cd-fixture-testing-strategy]], [[RN-05-oauth2-token-lifecycle]]
- Related: [[RN-10-prompt-injection-mitigation]], [[quality-and-quota-governance]]
- Entry point: [[index]]
