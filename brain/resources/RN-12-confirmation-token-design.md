---
id: RN-12
title: "Confirmation Token and Human-Consent Design for Gated Playlist Writes"
type: research
stage: 2
author: "Raj Gandhi (rajg2906)"
created: "2026-11-26"
requirements: ["FR-5", "REQ-5.3", "REQ-5.4", "SAF-3", "NFR-4"]
issues: ["#20", "#5", "#9"]
prs: []
---

# RN-12: Confirmation Token and Human-Consent Design for Gated Playlist Writes

## 1. Core Concepts & Findings
- A token returned in a tool result is visible to the model. It can prove that a proposal exists
  and was not altered; it cannot prove that a human approved it. Both properties are needed.
- Integrity: bind the token to the proposal ID, the exact ordered video IDs and the expiry with
  an HMAC (a keyed hash). The server recomputes the HMAC from its own stored proposal, so a
  client that changes the list or the expiry produces a mismatch. Compare with a constant-time
  function to avoid timing leaks.
- Replay: consume the token with a single atomic conditional update (`used = 0` to `used = 1`)
  before the first write; a second confirm finds `used = 1` and fails. Store only a hash of the
  token, so a leaked database does not leak usable tokens.
- Expiry: a short lifetime (default 15 minutes) limits the window for misuse; clock reads use
  one function so tests can fake time.
- Human consent: use the client's user-confirmation feature (MCP elicitation) when available;
  otherwise rely on the client's per-tool approval dialog by declaring the tool as a write tool.
  A free-text "yes" parameter is not proof because the model can supply it.
- Prompt injection can only influence what the model says; it cannot approve a dialog the
  client shows to the user, which is why the consent signal sits outside model-controlled text.

## 2. Architectural & Requirement Impact
- Defines the contract tested in SEC-4 and TQ-3 for FR-5; implemented by
  `services/confirmation.py` (`docs/architecture.md` sections 6, 9.2, 10); decision in ADR-0008.
- Risk DEP-2 (client must support multi-turn confirmation) is handled by a Stage 3 spike.

## 3. Connected Brain Nodes
- Source notes: [[RN-10-prompt-injection-mitigation]], [[RN-07-playlist-constraint-satisfaction]]
- Related: [[RN-05-oauth2-token-lifecycle]], [[quality-and-quota-governance]]
- Entry point: [[index]]
