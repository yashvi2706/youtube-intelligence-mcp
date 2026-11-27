# ADR-0008: Signed single-use confirmation token plus a human-consent signal

- Status: Proposed
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: FR-5, REQ-5.3, REQ-5.4, SAF-3, NFR-4, SEC-4, DEP-2
- Issues: Refs #20, Refs #5, Refs #9

## Context
No playlist may be written without explicit human confirmation, and hostile video metadata must
not be able to trigger or bypass that (REQ-5.4, SEC-4). A token returned to the AI client proves
only that a proposal exists; a model that has read the token could call the write tool itself.
The token therefore protects integrity, and a separate signal must prove a human said yes.

## Decision
1. **Token** (integrity, replay): on proposal, the server creates a random nonce and stores the
   proposal and its ordered video IDs. Token = `nonce` + HMAC-SHA256, computed with a server
   secret (kept outside the repo) over proposal ID, expiry, ordered video IDs and nonce. Only the
   token hash is stored. On confirm the server recomputes the HMAC from the *stored* proposal,
   compares in constant time, checks expiry (default 15 minutes) and consumes it with one
   conditional database update immediately before the first write.
2. **Human consent** (REQ-5.4a): `confirm_create_playlist` first asks the user through the MCP
   user-confirmation mechanism of the client (elicitation) when the client supports it. If the
   client does not, the tool is declared as a non-read-only, non-idempotent write tool so that
   the client's own tool-approval dialog is the human gate. The tool never accepts a free-text
   "user said yes" parameter as proof.
3. No untrusted text is ever placed in a field the model treats as an instruction (ADR-0009).
4. Stage 3 starts with a spike on the demo client (ADR-0003) to confirm which mechanism applies
   and records the result here; the status becomes Accepted then.

## Alternatives Considered
- Token only: rejected; does not prove a human was involved.
- Free-text confirmation phrase argument: rejected; the model can supply it.

## Consequences
- Depends on client capabilities (DEP-2); the risk and its mitigation are explicit.
- Tests: tampered list, expired token, replay, missing consent, injection text in titles
  (SEC-4), failure after playlist creation (REQ-5.8).

## Brain Citations
- [[RN-10-prompt-injection-mitigation]]
- [[RN-12-confirmation-token-design]]
