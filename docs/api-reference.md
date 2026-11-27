# MCP API Reference (design contract, v0.1 - Stage 2)

Developer API specification for the 8 tools and 3 resources in SRS section 3.3 (SE-7). This is the
**design contract** written before implementation; Stage 3 keeps it in sync with the code and
Stage 4 publishes the final version. Values marked **Proposed** are choices the SRS leaves open.
Error codes are defined in SRS section 6.4. Unit costs are from SRS section 2.5.

## 1. Conventions
- **Transport:** MCP over stdio (JSON-RPC 2.0).
- **Unknown fields are rejected** with `INVALID_PARAMETER` (NFR-9).
- **Video input** (`video`): watch URL, `youtu.be` URL or an 11-character ID `[A-Za-z0-9_-]{11}`.
- **Channel input** (`channel`): canonical channel URL, 24-character ID starting `UC`, or an
  `@handle` of 3 to 30 characters (letters, digits, `_`, `-`, `.`). Legacy `/c/` and `/user/`
  URLs are rejected locally.
- **limit:** integer 1 to 25, default 10. **language:** ISO 639-1 two-letter code.
- **Durations** in output are `MM:SS` or `HH:MM:SS`, with `duration_seconds` alongside.

### 1.1 Success envelope (Proposed)
```json
{
  "ok": true,
  "data": { },
  "markdown": "human-readable table",
  "quota": { "units_consumed": 0, "cache_hit": false, "remaining_today": 9900 },
  "untrusted_fields": ["items[].title", "items[].channel_title"]
}
```
Strings listed in `untrusted_fields` came from YouTube, are sanitized (ADR-0009) and must be
treated as data, never as instructions.

### 1.2 Error envelope (SRS 3.1 and 6.4)
```json
{
  "ok": false,
  "error": {
    "code": "QUOTA_BUDGET_EXCEEDED",
    "message": "Estimated 104 units but only 60 remain today.",
    "retryable": false,
    "hint": "Retry after the quota resets at the time shown in quota://status."
  }
}
```
`retryable` is true only where SRS 6.4 says "Yes".

## 2. Tools
### 2.1 `get_video_details` (REQ-1.7) - read-only, API key
| Param | Type | Rules |
| :--- | :--- | :--- |
| `video` | string | required; video input rules |

Returns `video_id`, `title`, `channel_title`, `duration`, `duration_seconds`, `category`, `tags`,
`description` (truncated to 1,000 characters). Cost: 1 unit (0 on cache hit).
Errors: `INVALID_VIDEO_ID`, `VIDEO_NOT_FOUND_OR_PRIVATE`, shared errors.

### 2.2 `find_similar_videos` (FR-1) - read-only, API key
| Param | Type | Rules |
| :--- | :--- | :--- |
| `video` | string | required |
| `limit` | integer | optional, 1 to 25, default 10 |

Returns ranked `items[]`: `video_id`, `title`, `channel_title`, `duration`, `score`,
`factors{text, category_topic, duration}`, `flags[]` (for example `missing_duration`),
`missing_fields[]`. Cost: about 104 units worst case (ADR-0004). Errors as REQ-1.6.

### 2.3 `find_similar_channels` (FR-2) - read-only, API key
| Param | Type | Rules |
| :--- | :--- | :--- |
| `channel` | string | required |
| `limit` | integer | optional, 1 to 25, default 10 |

Returns ranked `items[]`: `channel_id`, `handle`, `title`, `subscriber_count` or
`"hidden"`, `avg_upload_duration`, `shared_topics[]`, `score`,
`factors{text, topics, cadence, avg_duration}`. Cost: up to about 123 units.
Errors: `INVALID_IDENTIFIER`, `CHANNEL_NOT_FOUND`, shared errors.

### 2.4 `recommend_videos` (FR-3) - read-only, OAuth `youtube.readonly`
| Param | Type | Rules |
| :--- | :--- | :--- |
| `limit` | integer | optional, 1 to 25, default 10 |
| `focus_topic` | string | optional, 1 to 100 characters; allows one cached search (100 units) |

Returns `items[]` with `video_id`, `title`, `channel_title`, `duration`, `score`, `rationale`
(plain English: matching topics, duration fit, source channel). Excludes liked and saved videos.
Cost: about 20 to 60 units, up to about 160 with `focus_topic`.
Errors: `REAUTH_REQUIRED`, `INSUFFICIENT_PROFILE_DATA`, shared errors.

### 2.5 `analyze_engagement` (FR-4) - read-only, OAuth `youtube.readonly`
| Param | Type | Rules |
| :--- | :--- | :--- |
| `window_days` | integer | optional, 7 to 730, default 90 |

Returns the five views of REQ-4.3: `top_channels`, `top_categories`, `trends`,
`duration_preferences` (mean, median, IQR, four buckets), `period_delta`; plus
`timestamp_sources` counts (ADR-0011). Empty windows return zero counts, not an error.
Cost: about 20 to 60 units. Errors: `INVALID_PARAMETER`, `REAUTH_REQUIRED`, shared errors.

### 2.6 `propose_playlist` (FR-5 step 1) - read-only, API key
| Param | Type | Rules |
| :--- | :--- | :--- |
| `topic` | string | required, 1 to 200 characters |
| `max_total_minutes` | integer | required, **Proposed** 5 to 1440 |
| `max_video_minutes` | integer | required, **Proposed** 1 to `max_total_minutes` |
| `language` | string | required, ISO 639-1 |
| `seed_video` | string | optional, video input rules |
| `allow_unknown_language` | boolean | optional, default false |
| `playlist_title` | string | optional, up to 150 characters |

Performs zero writes. Returns `proposal_id`, `confirmation_token`, `expires_at`,
`tracklist[]` (position, `video_id`, title, channel, duration, relevance), `total_duration`,
`creation_cost_units` (50 + 50 x N) and a confirmation prompt. Cost: about 103 units.
Errors: `NO_COMPLIANT_PLAYLIST`, `INVALID_PARAMETER`, shared errors.

### 2.7 `confirm_create_playlist` (FR-5 step 2) - write, gated, OAuth write scope
| Param | Type | Rules |
| :--- | :--- | :--- |
| `proposal_id` | string | required |
| `confirmation_token` | string | required |

Verifies human consent (ADR-0008), then the token, expiry, single use and quota
(50 + 50 x N units), creates a **private** playlist and inserts videos in order. Returns
`playlist_url` and `video_ids`. Errors: `CONFIRMATION_REQUIRED`, `PROPOSAL_INVALID_OR_EXPIRED`,
`YOUTUBE_CHANNEL_REQUIRED`, `REAUTH_REQUIRED`, `QUOTA_BUDGET_EXCEEDED`,
`PLAYLIST_PARTIALLY_CREATED` (returns playlist URL, inserted IDs, missing IDs), shared errors.
Annotations: not read-only, not idempotent.

### 2.8 `analyze_playlist` (REQ-5.5) - read-only
| Param | Type | Rules |
| :--- | :--- | :--- |
| `proposal_id` | string | exactly one of `proposal_id` / `playlist_id` |
| `playlist_id` | string | exactly one of the two; private playlists need OAuth |

Returns total, mean and median duration, unique channel count, category distribution and the
four duration buckets (under 5, 5 to under 20, 20 to under 60, 60 and over minutes). Cost: 0 for a
proposal, about 2 units for a playlist. Errors: `PROPOSAL_INVALID_OR_EXPIRED`,
`REAUTH_REQUIRED`, `INVALID_PARAMETER`, shared errors.

## 3. Resources
| URI | Content | Cost | Errors |
| :--- | :--- | :--- | :--- |
| `youtube://video/{id}` | Same payload as `get_video_details` (REQ-1.8) | 1 unit | `INVALID_VIDEO_ID`, `VIDEO_NOT_FOUND_OR_PRIVATE` |
| `youtube://channel/{id}` | Channel ID, handle, title, truncated description, subscribers or hidden, topics (REQ-2.6) | 1 unit | `INVALID_IDENTIFIER`, `CHANNEL_NOT_FOUND` |
| `quota://status` | Daily limit, committed, reserved, remaining, next reset time (SAF-1) | 0 | none |

## 4. Shared errors
`INVALID_PARAMETER`, `QUOTA_BUDGET_EXCEEDED`, `QUOTA_EXCEEDED`, `RATE_LIMITED`,
`UPSTREAM_UNAVAILABLE` apply to every tool. Full table: SRS section 6.4.
