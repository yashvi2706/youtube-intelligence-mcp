# ADR-0002: Provider interface, fixture provider and decorators

- Status: Accepted
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: NFR-1, NFR-6, NFR-10, SE-6, TQ-2, TQ-5
- Issues: Refs #20, Refs #6

## Context
All YouTube access must sit behind one interface so the server runs offline in CI (SE-6, TQ-5).
`providers/base.py` has two abstract methods, `get_video_metadata` and `search_videos`, covered by
the Stage 1 smoke test. The SRS needs more operations (channels, uploads, user data, writes), a
quota meter (NFR-2) and a cache (NFR-10), and none of these may leak into the Intelligence Layer.

## Decision
1. Extend `YouTubeProvider` with the methods listed in `docs/architecture.md` section 6/7,
   returning typed dataclasses (`models.py`) instead of raw dictionaries.
2. Keep `get_video_metadata` and `search_videos` unchanged so the Stage 1 test stays valid; they
   are thin conveniences over `get_videos` and `search`.
3. Provide `LiveYouTubeProvider` (official API client) and `FixtureProvider` (recorded JSON from
   `tests/fixtures/`, including recorded error cases).
4. Add cross-cutting behaviour as decorators implementing the same interface:
   `CachedProvider(MeteredProvider(inner))`. `MeteredProvider` charges the quota ledger from a
   cost table; `CachedProvider` serves hits at 0 units.
5. Only `server.py` selects the concrete provider from `YOUTUBE_PROVIDER_MODE`.

## Alternatives Considered
- Mock the Google client in each test: rejected; duplicates setup and does not exercise the
  metering and cache paths.
- Put caching/metering inside the live provider: rejected; the fixture path would skip them and
  TQ-2/TQ-6 could not be tested offline.

## Consequences
- Every new YouTube operation is one interface method, one fixture set and one cost-table row.
- Fixture mode also meters "virtual units", so TQ-6 runs in CI.
- The interface grows in Stage 3; abstract-method additions must not break the existing test.

## Brain Citations
- [[RN-01-mcp-protocol-architecture]]
- [[RN-09-ci-cd-fixture-testing-strategy]]
