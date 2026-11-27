# ADR-0010: OAuth credential storage, scopes and re-authorisation

- Status: Accepted
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: NFR-3, NFR-7, SEC-1, SEC-2, REQ-3.4, REQ-5.4, TQ-4
- Issues: Refs #20, Refs #8

## Context
OAuth tokens in Testing mode expire after 7 days. Read tools must use `youtube.readonly`, and
write scope is only for confirmed playlist creation. Secrets must never enter the repository,
fixtures, logs or AI tools. The SRS names Windows, Linux and macOS as host systems.

## Decision
1. Client secret and token file paths come from `YOUTUBE_CLIENT_SECRET_PATH` and
   `YOUTUBE_TOKEN_PATH`; both are outside the repository; `.gitignore` and the CI secret scan
   back this up.
2. The first sign-in requests `youtube.readonly` only. The write scope is requested by an explicit
   upgrade step the first time a confirmed creation needs it; a token without it yields
   `REAUTH_REQUIRED` with a hint.
3. Token files are created with owner-only permissions (`0600`) on Linux/macOS. Windows cannot
   enforce POSIX modes; Stage 3 verifies a Windows ACL approach and records the outcome here.
4. Expired, revoked or missing tokens, and `invalid_grant` responses, raise `REAUTH_REQUIRED`.
   The server never starts a browser flow inside a tool call; a separate CLI command signs in.
5. Public tools (FR-1, FR-2, proposal step) use the API key and never touch user tokens.
6. Tokens, secrets and authorization headers are redacted from logs and error messages.

## Alternatives Considered
- Request write scope up front: rejected; violates least privilege for read-only tools.
- Browser flow inside a tool call: rejected; blocks the MCP session and is unsafe for headless runs.

## Consequences
- SEC-1 test: read-only tools never request a write scope; storage test checks permissions where
  the OS supports them.
- Team members must be listed as test users on the consent screen (AS-1).
- An unresolved Windows permission method is tracked as a Stage 3 task.

## Brain Citations
- [[RN-05-oauth2-token-lifecycle]]
