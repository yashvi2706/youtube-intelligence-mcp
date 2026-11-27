# ADR-0011: Activity timestamp source for engagement analysis

- Status: Proposed
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: FR-4, REQ-4.2, REQ-4.3, TBD-3
- Issues: Refs #20, Refs #4

## Context
FR-4 compares time windows, so each interaction needs a date. REQ-4.2 prefers the subscription
creation date, the playlist-item addition date and a like timestamp, and falls back to the
video's publication date with a visible note. Whether liked videos expose a reliable like time
through the official API is unverified (TBD-3), and this document does not assume it.

## Decision
1. Subscriptions use the subscription creation time; playlist items use the time the item was
   added to the playlist, when the API returns it.
2. For liked videos, the Stage 3 spike (first live-API task) inspects the real responses for the
   user's liked-videos list and records whether a per-item time is present. If it is, it is used;
   if not, publication date is the fallback.
3. Whatever source is used, each activity record carries `timestamp_source` and the output states
   how many records used the fallback, as REQ-4.2 requires.
4. This ADR is updated to Accepted with the observed behaviour once the spike is complete.

## Alternatives Considered
- Assume a like timestamp exists: rejected; unverified.
- Drop trend views when timestamps are missing: rejected; REQ-4.2 already defines a fallback.

## Consequences
- Trend and period-over-period results for likes may reflect publication dates rather than like
  dates; the response says so.
- Fixtures include records with and without per-item times.

## Brain Citations
- [[RN-06-engagement-analytics-metrics]]
