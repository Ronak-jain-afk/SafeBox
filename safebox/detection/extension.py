"""Detect language from file extension."""

from __future__ import annotations

from pathlib import Path

from safebox.config.constants import EXTENSION_MAP


def detect_by_extension(script_path: Path) -> str | None:
    """Return the canonical language name based on file extension, or None."""
    suffix = script_path.suffix.lower()
    return EXTENSION_MAP.get(suffix)
