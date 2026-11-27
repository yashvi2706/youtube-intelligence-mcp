# ADR-0007: Playlist selection as a bounded knapsack on rounded-up durations

- Status: Accepted
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: FR-5, REQ-5.1, REQ-5.2, REQ-5.6, NFR-8, TQ-1
- Issues: Refs #20, Refs #5

## Context
REQ-5.2 requires the compliant subset with the highest total relevance whose total duration does
not exceed the cap, rounding durations up so the real total never exceeds the cap, and
`NO_COMPLIANT_PLAYLIST` when no non-empty subset fits. Selection must stay under 500 ms for 200
candidates (NFR-8).

## Decision
1. Hard filters first (REQ-5.1): drop videos longer than the single-video limit, with a language
   other than the requested ISO 639-1 code, with missing language (unless explicitly allowed),
   with zero duration (live streams) and duplicates.
2. Convert each duration to units of 15 seconds with `ceil`, and the cap with `floor`. Run a
   0/1 knapsack dynamic programme: weight = rounded units, value = relevance.
   Cost is `candidates x cap_units` (for 200 videos and 2 hours: 200 x 480 cells).
3. Determinism: sort candidates by relevance descending then video ID; keep a strictly-better
   comparison so the first optimal solution wins; reconstruct the chosen set from the table.
4. Output order: relevance descending, ties by video ID (an ordering policy the SRS leaves open;
   it can be revisited without changing the selection).
5. If the chosen set is empty, raise `NO_COMPLIANT_PLAYLIST`.

## Alternatives Considered
- Greedy by relevance density: not optimal, may under-fill the cap.
- Exact DP at one-second granularity: 7,200 x 200 cells, risks the NFR-8 time budget in pure
  Python for long caps; 15 s granularity loses at most 14 s per video, which is acceptable.

## Consequences
- The real total can be up to 14 s per video below the rounded total; it never exceeds the cap.
- Unit tests: optimality against brute force for small sets, rounding-up property, tie-breaking,
  empty result, performance with 200 candidates.

## Brain Citations
- [[RN-07-playlist-constraint-satisfaction]]
