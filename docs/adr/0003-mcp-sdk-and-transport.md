# ADR-0003: Use the official MCP Python SDK over stdio

- Status: Proposed
- Date: 2026-11-26
- Deciders: Yashvi Mehta, Dhyan Patel, Raj Gandhi
- Requirements: NFR-11, SRS 3.4, DEP-2, TQ-3
- Issues: Refs #20

## Context
SRS 3.4 requires JSON-RPC 2.0 over stdio, with an optional loopback HTTP/SSE transport for the MCP
Inspector. The repository is Python (`requires-python >= 3.10`, CI on 3.11). The team has not yet
fixed an SDK or demo client. Tool schemas, resources and the user-confirmation mechanism depend
on what the SDK and client support, and the exact SDK API must be checked against its current
documentation before code is written.

## Decision
Use the official MCP Python SDK (package `mcp`) with its high-level server API, stdio transport
first. Demo and Stage 4 client: Claude Desktop, with the MCP Inspector for debugging. Pin the SDK
version in `pyproject.toml` after a Stage 3 spike. The status becomes Accepted when the spike
proves (a) tools, resources and annotations register, (b) stdio works under Claude Desktop, and
(c) the confirmation mechanism in ADR-0008 is available.

## Alternatives Considered
- Hand-written JSON-RPC server: rejected; more code to maintain and test for no benefit.
- HTTP/SSE as the primary transport: rejected; not required by the SRS and adds network exposure.

## Consequences
- Adds a runtime dependency (`mcp`); `pyproject.toml` currently has none.
- Tests in `tests/system/` drive tools through the MCP interface (TQ-3), for example through the
  SDK's client session or an in-memory transport.
- If the spike fails, this ADR is superseded and the design layers above `server.py` are unchanged.

## Brain Citations
- [[RN-01-mcp-protocol-architecture]]
