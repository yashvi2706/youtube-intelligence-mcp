---
id: RN-02
title: "YouTube Data API v3 Endpoints, Constraints & Error Taxonomy"
type: research
stage: 1
author: "Member-1"
created: "2026-11-06"
requirements: ["FR-1", "FR-2", "FR-3", "FR-4", "FR-5", "NFR-5"]
issues: ["#1", "#2", "#10"]
prs: ["#102"]
---

# RN-02: YouTube Data API v3 Endpoints, Constraints & Error Taxonomy

## 1. Core Concepts & Findings
- The official YouTube Data API v3 does **not** expose user watch history and deprecated the `relatedToVideoId` parameter in `search.list`.
- Core endpoints required for our MCP server:
  - `videos.list` (`part=snippet,contentDetails,statistics,topicDetails`): Fetches rich metadata for up to 50 video IDs per call (Cost: **1 unit**). Also supports `myRating=like` to fetch a user's liked videos.
  - `channels.list` (`part=snippet,statistics,topicDetails,brandingSettings,contentDetails`): Resolves `@handle` (`forHandle`) or channel ID (Cost: **1 unit**).
  - `subscriptions.list` (`part=snippet`, `mine=true`): Lists user's subscribed channels (Cost: **1 unit**).
  - `playlists.list` & `playlistItems.list` (Cost: **1 unit** each): Reads user playlists or a channel's `uploads` playlist.
  - `search.list` (`part=snippet`, `type=video|channel`): Keyword discovery (Cost: **100 units**).
  - `playlists.insert` & `playlistItems.insert` (Cost: **50 units** each): Creates a playlist and adds videos.

## 2. Architectural & Requirement Impact
- Directly governs `FR-1` through `FR-5` and `NFR-5` (`TQ-4`).
- Negative test cases (`TQ-4`) must explicitly trap HTTP 403 `quotaExceeded`, HTTP 400/403 `youtubeSignupRequired` (when a Google account has no YouTube channel), HTTP 401 expired OAuth token, and empty `items: []` for private/deleted videos.

## 3. Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[RN-01-mcp-protocol-architecture]], [[RN-03-youtube-quota-budget-management]], [[RN-04-tfidf-cosine-similarity-design]]