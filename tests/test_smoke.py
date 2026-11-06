# File: tests/test_smoke.py
"""Stage 1 CI smoke test verifying package layout and provider abstraction (SE-6)."""

from youtube_mcp import __version__
from youtube_mcp.providers.base import YouTubeProvider


def test_version_and_provider_interface() -> None:
    assert __version__ == "0.1.0"
    assert hasattr(YouTubeProvider, "get_video_metadata")
    assert hasattr(YouTubeProvider, "search_videos")