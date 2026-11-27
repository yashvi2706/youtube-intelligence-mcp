# ADR-0006: Similarity scoring design (TF-IDF, cosine, weighted metadata)

- Status: Accepted
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: FR-1, FR-2, FR-3, REQ-1.3, REQ-1.4, REQ-1.5, REQ-2.2, NFR-8
- Issues: Refs #20, Refs #1, Refs #2

## Context
The YouTube API has no related-videos or related-channels endpoint, so the server computes
similarity from metadata (SRS 2.5). The SRS fixes only the order of factor weights and requires
deterministic output within 500 ms for 200 candidates; formulas were deferred to this stage.

## Decision
**Text vector.** Tokenise lower-cased text with a Unicode word regex and a small stop-word list.
Build one term-frequency bag per item with field multipliers: title x3, tags x2, description x1
(videos); channel title x3, topic keywords x2, description and recent upload titles x1 (channels).
Use sublinear TF `1 + ln(tf)` and smoothed IDF `ln((1 + N) / (1 + df)) + 1`, with N the number of
documents in the seed-plus-candidate set. Text similarity is the cosine of the seed vector and a
candidate vector (range 0 to 1 because all weights are non-negative). Pure Python, no NumPy.

**FR-1 composite** (weights sum to 1, descending order as the SRS requires):
`score = 0.60 x text + 0.25 x category_topic + 0.15 x duration`.
- `category_topic` is the Jaccard overlap of topic categories; if the category IDs are equal the
  value is raised to at least 0.5.
- `duration` is `min(d_seed, d_cand) / max(d_seed, d_cand)`.
- Missing fields (REQ-1.4): drop the missing factor and re-normalise the remaining weights; zero
  or missing candidate duration gives duration credit 0 and a flag; missing seed duration drops
  the duration factor for every candidate.

**FR-2 composite:** `0.50 x text + 0.30 x shared_topics + 0.10 x cadence + 0.10 x avg_duration`,
where cadence and average duration use the same min/max ratio on uploads per week and mean
duration of the latest 10 uploads.

**Ordering.** Sort by score descending, ties by ID ascending (REQ-1.5); scores are rounded to
6 decimals before sorting so floating-point noise cannot reorder results. The seed is excluded.
Each result exposes the composite and every factor score.

## Alternatives Considered
- scikit-learn `TfidfVectorizer`: rejected; heavy install in CI, harder to explain line by line.
- Embeddings or an LLM re-ranker: rejected; not allowed by the "simple techniques" note, not
  deterministic, costs extra network calls.

## Consequences
- Weights are defaults; Stage 3 tunes them against fixtures but must keep the SRS order.
- Property tests: self-similarity is 1.0, scores in [0, 1], identical input gives identical order,
  200 candidates run under 500 ms (NFR-8).
- The Jaccard-plus-category rule is a deliberate simplification and is documented for reviewers.

## Brain Citations
- [[RN-04-tfidf-cosine-similarity-design]]
