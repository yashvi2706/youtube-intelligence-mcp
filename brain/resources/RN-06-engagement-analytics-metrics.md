---
id: RN-06
title: "User Engagement Analytics Metrics & Period-over-Period Deltas"
type: research
stage: 1
author: "Member-3"
created: "2026-11-06"
requirements: ["FR-4"]
issues: ["#4", "#12"]
prs: ["#103"]
---

# RN-06: User Engagement Analytics Metrics & Period-over-Period Deltas

## 1. Core Concepts & Findings
To fulfill `FR-4`, the server aggregates metadata across three authorized collections—Liked Videos, Subscriptions, and Playlists—and computes five quantitative dimensions:
1. **Top Channels:** Frequency distribution of channels in liked/playlisted items plus overlap ratio with active subscriptions.
2. **Top Categories:** Percentage share by YouTube `categoryId` (e.g., `27` Education, `28` Science & Technology) and `topicCategories`.
3. **Trends Over Time:** Time-bucketed counts (by month/week) of engagement timestamps (`snippet.publishedAt` on playlist items and subscription dates).
4. **Duration Preferences:** Mean, median, P25/P75 quartiles, and bucket histogram (`Short <5m`, `Focused 5-20m`, `Standard 20-60m`, `Extended >60m`).
5. **Period-over-Period Comparison:** Compares window $W_{\text{current}} = [T - \Delta, T]$ against $W_{\text{previous}} = [T - 2\Delta, T - \Delta]$ to surface topic growth and runtime shifts.

## 2. Architectural & Requirement Impact
- Provides deterministic statistical outputs for `FR-4` that directly inform the user preference vector in `FR-3`.

## 3. Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[RN-02-youtube-data-api-v3-endpoints]], [[RN-04-tfidf-cosine-similarity-design]]