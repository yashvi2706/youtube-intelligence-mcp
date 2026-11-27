# ADR-0004: Pre-flight quota estimation with reserve and commit

- Status: Accepted
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: NFR-2, SAF-1, TQ-6, REQ-3.2, REQ-5.4
- Issues: Refs #20, Refs #7

## Context
A request that would exceed the daily budget must be rejected before any YouTube call
(SAF-1, TQ-6). `search.list` costs 100 units and a playlist write costs 50 + 50 x N units.

## Decision
1. `QuotaEstimator.estimate(tool, params)` returns the worst-case units for a request from a
   cost table (the SRS 2.5 values) and the request parameters (batch counts, page caps, N videos).
2. At the start of a tool call the server calls `QuotaLedger.reserve(estimate)`. If
   `committed + reserved + estimate > limit` it raises `QUOTA_BUDGET_EXCEEDED` and nothing else runs.
3. `MeteredProvider` records actual units per call; at the end of the tool the ledger commits the
   actual total and releases the unused reservation. Cache hits add 0.
4. Each calendar day is the Pacific-time date (the YouTube reset boundary). Limit comes from
   `YOUTUBE_DAILY_QUOTA_LIMIT` (default 10000).
5. `quota://status` reads committed, reserved, remaining and the next reset time.
6. A real `quotaExceeded` from YouTube maps to `QUOTA_EXCEEDED` and forces the ledger to
   "exhausted" for the rest of the day.

## Alternatives Considered
- Count only after calls: rejected; violates the "before any API call" requirement.
- In-memory counter: rejected; loses usage on restart and breaks the 10,000-unit guarantee.

## Consequences
- Estimates are upper bounds, so a request may be refused while actual cost would have fit; this
  is accepted (quota safety outranks throughput).
- Estimator tables need a unit test per tool (TQ-1) and a refusal test (TQ-6).
- The ledger tracks only this server's usage; calls made outside it with the same project are
  invisible, which `quotaExceeded` handling covers.

## Brain Citations
- [[RN-03-youtube-quota-budget-management]]
