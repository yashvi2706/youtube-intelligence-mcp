# ADR-0009: One sanitizer for all YouTube-originated text

- Status: Accepted
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: NFR-4, NFR-9, SEC-4, SEC-5, REQ-1.7, REQ-1.8, REQ-2.6
- Issues: Refs #20, Refs #9

## Context
Titles, descriptions, tags and channel names are written by third parties and are returned to an
LLM client, so they can carry prompt-injection text. NFR-4 sets the minimum: strip control
characters and instruction-like delimiters, truncate (titles and channel names 200, descriptions
1,000, tags 100 characters) and wrap in data boundaries.

## Decision
1. `sanitize.py` is the only module that turns raw provider text into output text; every tool and
   resource calls it, and a unit test asserts no tool returns an unsanitized field.
2. Steps: Unicode NFKC normalisation; remove control and format characters (including zero-width
   and bidirectional overrides) except space; collapse whitespace; neutralise instruction-like
   delimiters (code fences, XML-like tags, chat-role prefixes, `<|...|>` markers) by escaping;
   truncate at the NFR-4 limits with an ellipsis marker.
3. Output shape: untrusted strings appear only as values of named data fields in the JSON payload;
   the envelope has an explicit `untrusted_fields` list. Markdown tables escape pipes and
   backticks. Untrusted text never appears in `message`, `hint` or tool descriptions.
4. Sanitization is idempotent and runs again on cached payloads before output.

## Alternatives Considered
- Pattern blocklist of known attack phrases: rejected as the only defence (easy to evade); kept
  only as extra neutralisation.
- Output filtering by the client: not under our control.

## Consequences
- Property tests: idempotence, length bounds, no control characters, no unescaped delimiters.
- Fixtures include hostile titles and descriptions (SEC-4) and contain no real user data (SEC-5).

## Brain Citations
- [[RN-10-prompt-injection-mitigation]]
