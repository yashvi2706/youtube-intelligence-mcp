---
id: RN-07
title: "Constraint-Based Playlist Curation & Bounded Knapsack Selection"
type: research
stage: 1
author: "Member-3"
created: "2026-11-06"
requirements: ["FR-5", "SK-5", "NFR-8"]
issues: ["#5", "#12"]
prs: ["#103"]
---

# RN-07: Constraint-Based Playlist Curation & Bounded Knapsack Selection

## 1. Core Concepts & Findings
`FR-5` requires constructing a playlist from natural-language constraints:
- **Hard Individual Filters:**
  - Runtime filter: $d_i \le D_{\max\_video}$ (e.g., no video over 20 minutes).
  - Language filter: `defaultAudioLanguage` or `defaultLanguage` matches target ISO 639-1 code (e.g., `en`).
- **Combinatorial Optimization (0/1 Knapsack):**
  - Given candidate videos with relevance score $v_i$ and duration $d_i$ (discretized into 15-second blocks), select subset $S$ maximizing $\sum_{i \in S} v_i$ subject to $\sum_{i \in S} d_i \le D_{\text{total}}$.
  - Diversity penalty prevents a single channel from dominating more than 40% of the playlist unless requested.

## 2. Architectural & Requirement Impact
- Powers both `FR-5` and `SK-5` (`video-to-playlist`).
- Produces a deterministic proposal with a cryptographic `confirmation_token` before any write call (`playlists.insert`) is permitted.

## 3. Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[RN-04-tfidf-cosine-similarity-design]], [[RN-10-prompt-injection-mitigation]]