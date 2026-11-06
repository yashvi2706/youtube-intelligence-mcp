# AGENTS.md — AI-Assisted Engineering & Second Brain Governance

## 1. Project Overview
This repository contains the **YouTube Video Intelligence MCP Server**, an MCP-compatible server that connects AI clients (Claude, ChatGPT, Gemini) to the official YouTube Data API v3 through an isolated provider interface (`SE-6`) to discover similar videos/channels, analyze user engagement, and curate constraint-based playlists.

## 2. Second Brain Vault Rules (PARA & Schema)
The `brain/` directory is an Obsidian vault structured using the **PARA** method:
- `brain/inbox/`: Unsorted incoming notes awaiting refinement.
- `brain/projects/`: Active stage deliverables, sprint plans, and stage review notes (`SB-2`).
- `brain/areas/`: Ongoing engineering responsibilities (security, quota governance, CI quality).
- `brain/resources/`: Distilled technical research notes (`RN-01` through `RN-10`) and `ai-session` logs.
- `brain/archive/`: Inactive or superseded material.
- `brain/index.md`: Primary entry point to the knowledge graph.
- `brain/log.md`: Chronological execution log of all `brain-ingest`, `brain-refine`, and `brain-query` runs.

### Mandatory Note Frontmatter Schema
Every Markdown note inside `brain/` (except `index.md` and `log.md`) MUST begin with YAML frontmatter containing:
```yaml
---
id: RN-XX
title: "Descriptive Note Title"
type: research | project | area | review | ai-session
stage: 1
author: "Team Member Name / Git Handle"
created: "2026-11-06"
requirements: ["FR-1", "NFR-1"]
issues: ["#1", "#12"]
prs: ["#101"]
---