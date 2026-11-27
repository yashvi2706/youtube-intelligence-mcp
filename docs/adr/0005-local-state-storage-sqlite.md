# ADR-0005: Keep local state in one SQLite database (WAL mode)

- Status: Accepted
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: NFR-2, NFR-10, REQ-5.3, REQ-5.4, NFR-7
- Issues: Refs #20, Refs #7

## Context
The server must persist the quota ledger, the response cache and playlist proposals (with their
one-time tokens) across restarts and between concurrent tool calls, outside the repository. The
SDLC handout points to SQLite (ACID transactions, locking, WAL).

## Decision
Use the standard-library `sqlite3` module with one database file in the state directory
(`YOUTUBE_MCP_HOME`, outside the repo, owner-only permissions where the OS supports them), WAL
mode, and short transactions. Tables: `quota_ledger`, `cache_entry`, `proposal`, `proposal_item`
(`docs/architecture.md` section 11). Token consumption is a single conditional `UPDATE` so two
confirms cannot both succeed.

## Alternatives Considered
- JSON files: rejected; no atomic compare-and-set for tokens or reservations.
- External database or Redis: rejected; overkill for a single-user local server.
- In-memory only: rejected; loses budget and proposals on restart.

## Consequences
- No new dependency; tests use a temporary directory per test.
- A schema version row is added so Stage 3 migrations are explicit.
- Cached user-profile data lives in the same file; it must never be logged or committed.

## Brain Citations
- [[RN-03-youtube-quota-budget-management]]
- [[RN-05-oauth2-token-lifecycle]]
