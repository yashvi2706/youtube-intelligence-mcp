---
id: RN-04
title: "Metadata Feature Vectors, TF-IDF Weighting & Cosine Similarity"
type: research
stage: 1
author: "Member-2"
created: "2026-11-06"
requirements: ["FR-1", "FR-2", "FR-3", "NFR-8"]
issues: ["#1", "#2", "#3"]
prs: ["#102"]
---

# RN-04: Metadata Feature Vectors, TF-IDF Weighting & Cosine Similarity

## 1. Core Concepts & Findings
Because YouTube Data API v3 provides no native similarity endpoint, similarity must be computed deterministically over video and channel metadata:
1. **Text Corpus Construction:** Concatenate weighted text fields for each item: `Title` (repeated 3x for higher term weight), `Tags` (repeated 2x), and `Description` (1x, stripped of URLs and boilerplate).
2. **TF-IDF + Cosine Similarity ($S_{\text{text}}$):** Compute sublinear TF-IDF vectors with English stop-word removal and L2 normalization; dot product yields cosine similarity in $[0, 1]$.
3. **Categorical & Topic Similarity ($S_{\text{cat}}$):** Combine exact `categoryId` match (0.5) and Jaccard similarity over Wikipedia `topicCategories` URIs (0.5).
4. **Duration Proximity ($S_{\text{dur}}$):** Compute Gaussian similarity $\exp(-\frac{(\ln(d_1) - \ln(d_2))^2}{2\sigma^2})$ over ISO 8601 video runtimes so a 15-minute tutorial matches 12–20 minute tutorials rather than 30-second Shorts or 4-hour streams.

## 2. Architectural & Requirement Impact
- Composite score for `FR-1`: $S = 0.55 \cdot S_{\text{text}} + 0.25 \cdot S_{\text{cat}} + 0.20 \cdot S_{\text{dur}}$.
- Meets `NFR-8` by running in-memory vector operations in under 50 ms for 200 candidate videos.

## 3. Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[RN-02-youtube-data-api-v3-endpoints]], [[RN-06-engagement-analytics-metrics]], [[RN-07-playlist-constraint-satisfaction]]