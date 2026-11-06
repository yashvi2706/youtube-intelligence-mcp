# File: src/youtube_mcp/providers/base.py
"""Abstract YouTubeProvider interface (SE-6 & NFR-1)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class YouTubeProvider(ABC):
    """Isolates all external YouTube Data API v3 calls behind an interface."""

    @abstractmethod
    def get_video_metadata(self, video_id: str) -> dict[str, Any]:
        """Fetch metadata for a single video ID."""

    @abstractmethod
    def search_videos(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        """Search candidate videos matching a query string."""