---
id: RN-05
title: "OAuth 2.0 Minimum Scopes, 7-Day Testing Expiry & Security"
type: research
stage: 1
author: "Member-2"
created: "2026-11-06"
requirements: ["FR-3", "FR-5", "NFR-3", "NFR-7"]
issues: ["#3", "#8"]
prs: ["#102"]
---

# RN-05: OAuth 2.0 Minimum Scopes, 7-Day Testing Expiry & Security

## 1. Core Concepts & Findings
- Personal user data endpoints (`myRating=like`, `subscriptions.list`, `playlists.list` with `mine=true`) and write endpoints (`playlists.insert`) require OAuth 2.0 user authorization.
- **7-Day Testing Mode Expiry:** Google Cloud OAuth apps in `Testing` publishing status issue refresh tokens that strictly expire after **7 days** (`invalid_grant` on token refresh).
- **Least-Privilege Scopes:**
  - Read-only analysis (`FR-1` to `FR-4`): `https://www.googleapis.com/auth/youtube.readonly`
  - Playlist creation (`FR-5`): `https://www.googleapis.com/auth/youtube`

## 2. Architectural & Requirement Impact
- Satisfies `NFR-3` and `NFR-7`: OAuth tokens are stored outside the repository (configured via `YOUTUBE_TOKEN_PATH` in `.env`), and the auth wrapper traps `invalid_grant` / HTTP 401 to return a structured re-authentication instruction instead of crashing.

## 3. Connected Brain Nodes
- Entry Point: [[index]]
- Related Notes: [[RN-02-youtube-data-api-v3-endpoints]], [[RN-10-prompt-injection-mitigation]], [[quality-and-quota-governance]]