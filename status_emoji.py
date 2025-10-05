from __future__ import annotations
from typing import Dict, Optional


STATUS_EMOJI_MAP: Dict[int, str] = {
        1: "ℹ️",  # 1xx informational
        2: "✅",  # 2xx success
        3: "🔀",  # 3xx redirect
        4: "⛔",  # 4xx client error
        5: "💥",  # 5xx server error
    }


class StatusEmoji:
    """Class to map HTTP status codes to emojis."""

    def __init__(self, mapping: Optional[Dict[int, str]] = None, fallback: str = "❓"):
        self._mapping = dict(mapping or STATUS_EMOJI_MAP)
        self._fallback = fallback

    def get_emoji(self, status_code: int) -> str:
        try:
            family = int(status_code) // 100
        except (TypeError, ValueError):
            return self._fallback
        return self._mapping.get(family, self._fallback)

    __call__ = get_emoji



