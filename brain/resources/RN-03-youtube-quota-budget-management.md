---
id: RN-03
title: "10,000-Unit Quota Accounting, Caching & Pre-Flight Rejection"
type: research
stage: 1
author: "Member-2"
created: "2026-11-06"
requirements: ["NFR-2", "TQ-6"]
issues: ["#7", "#12"]
prs: ["#102"]
---

# RN-03: 10,000-Unit Quota Accounting, Caching & Pre-Flight Rejection

## 1. Core Concepts & Findings
A default Google Cloud project receives **10,000 quota units per day** (resets at midnight Pacific Time). Unchecked `search.list` (100 units) and `playlistItems.insert` (50 units/video) calls can exhaust the daily quota in fewer than 50 requests.
- **Cost Table:**
  - Read operations (`videos.list`, `channels.list`, `playlists.list`, `playlistItems.list`, `subscriptions.list`): **1 unit**
  - Write operations (`playlists.insert`, `playlistItems.insert`): **50 units**
  - Search operation (`search.list`): **100 units**

## 2. Architectural & Requirement Impact
- **Pre-Flight Quota Guardian (`NFR-2` / `TQ-6`):** Before executing any workflow, `QuotaBudgetManager.estimate_and_reserve(steps)` calculates total unit cost. If `used_units + estimated_cost > daily_budget`, the request raises `QuotaBudgetExceededError` **before** making a single network call.
- **Upload-Playlist Optimization:** For `FR-3` (Recommendations), fetching recent videos from subscribed channels via their `uploads` playlist (`playlistItems.list` = 1 unit) saves 99% of quota compared to `search.list` (100 units).

## 3. Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[RN-02-youtube-data-api-v3-endpoints]], [[RN-09-ci-cd-fixture-testing-strategy]], [[quality-and-quota-governance]]