---
id: RN-11
title: "Quota Ledger and Response Cache Storage Design"
type: research
stage: 2
author: "Dhyan Patel (dhyanspatel49)"
created: "2026-11-26"
requirements: ["NFR-2", "NFR-10", "SAF-1", "TQ-6"]
issues: ["#19", "#7"]
prs: []
---

# RN-11: Quota Ledger and Response Cache Storage Design

## 1. Core Concepts & Findings
- The daily budget resets at midnight Pacific Time, so the ledger is keyed by the Pacific
  calendar date, not by UTC. Python's `zoneinfo` handles this; Windows needs the `tzdata`
  package because it ships no system time zone database.
- A pre-flight check needs a counter that survives restarts. A single SQLite file gives atomic
  updates with no extra service. WAL mode lets readers (the `quota://status` resource) run while
  a writer updates the counter; WAL is described in the SQLite documentation listed in the SDLC
  handout.
- Reserve-then-commit avoids two concurrent requests both passing the check: `reserve(units)`
  runs inside one transaction that fails if `committed + reserved + units` exceeds the limit;
  after the call, `commit(actual)` converts the reservation and `release` frees what was unused.
- Cache entries carry an absolute expiry time. Reads ignore expired rows; a purge runs at startup.
  Default time-to-live values come from the SRS: 24 hours for video/channel metadata, 6 hours for
  search results, 1 hour for user profile data.
- Cache keys are a hash of method name and normalised arguments. User-specific entries include a
  non-reversible user key so two accounts never share data. Nothing from the cache is logged.

## 2. Architectural & Requirement Impact
- `QuotaLedger` and `ResponseCache` share `storage.py` (one connection helper, WAL on) —
  `docs/architecture.md` sections 4 and 11; decision in ADR-0005.
- The estimator is a pure function of tool name and parameters, so TQ-6 can assert a rejection
  without any provider call; `MeteredProvider` records actual cost for reconciliation.
- A cache hit reports 0 units, which TQ-2 asserts together with the under-20 ms target (NFR-10).

## 3. Connected Brain Nodes
- Source notes: [[RN-03-youtube-quota-budget-management]], [[RN-02-youtube-data-api-v3-endpoints]]
- Related: [[RN-09-ci-cd-fixture-testing-strategy]], [[quality-and-quota-governance]]
- Entry point: [[index]]
