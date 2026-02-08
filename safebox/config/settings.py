"""User configuration loader (TOML-based, ~/.safebox/config.toml)."""

from __future__ import annotations

from pathlib import Path

SAFEBOX_HOME = Path.home() / ".safebox"
PROFILES_DIR = SAFEBOX_HOME / "profiles"
LOGS_DIR = SAFEBOX_HOME / "logs"


def ensure_dirs() -> None:
    """Create SafeBox config directories if they don't exist."""
    SAFEBOX_HOME.mkdir(parents=True, exist_ok=True)
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
