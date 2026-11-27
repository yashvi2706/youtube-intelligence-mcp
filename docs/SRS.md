# Software Requirements Specification — Index

The authoritative SRS (v1.5.0, Stage 1 submission, Team forkBombers) is
[`docs/SRS.pdf`](SRS.pdf). This file is a lightweight index of its requirement IDs so that
documents and tools in the repository can link to them. If this index and the PDF disagree, the
PDF wins.

| Group | IDs | SRS section |
| :--- | :--- | :--- |
| System features | FR-1 Similar Videos, FR-2 Similar Channels, FR-3 Recommendations, FR-4 Engagement Analysis, FR-5 Playlist Creation with Confirmation | 4 |
| Detailed functional requirements | REQ-1.1 to REQ-1.8, REQ-2.1 to REQ-2.6, REQ-3.1 to REQ-3.4, REQ-4.1 to REQ-4.4, REQ-5.1 to REQ-5.8 | 4 |
| Nonfunctional | NFR-1 to NFR-13 | 5 |
| Safety | SAF-1 (= NFR-2), SAF-2, SAF-3 | 5.2 |
| Business rules | BR-1 to BR-4 | 5.5 |
| Agent skills | SK-1 brain-ingest, SK-2 brain-refine, SK-3 brain-query, SK-4 local-check, SK-5 video-to-playlist | 6.1 |
| Verification | TQ-1 to TQ-8, SEC-1 to SEC-5 | 6.2 |
| Errors | Structured error codes (INVALID_VIDEO_ID ... PLAYLIST_PARTIALLY_CREATED) | 6.4 |
| Open items | TBD-1 (issue/PR numbers), TBD-2 (live-test schedule), TBD-3 (activity timestamps) | Appendix C |

Known differences between the SRS and the repository are tracked in `docs/adr/` (for example
ADR-0001 on the `.skills/` folder name) and in `docs/traceability.md`.
