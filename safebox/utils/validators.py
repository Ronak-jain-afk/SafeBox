"""Input validators for CLI options."""

from __future__ import annotations

import re
from pathlib import Path

from safebox.config.constants import SUPPORTED_LANGUAGES


# ── Memory ────────────────────────────────────────────────────────────
_MEMORY_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*([kmgKMG])[bB]?$")

_MEMORY_UNITS = {"k": 1024, "m": 1024**2, "g": 1024**3}


def validate_memory(value: str) -> str:
    """Validate and normalise a memory string (e.g. ``512m``, ``1g``).

    Returns the normalised Docker-compatible form (lowercase, no `b`).
    Raises ``ValueError`` on bad input.
    """
    match = _MEMORY_RE.match(value.strip())
    if not match:
        raise ValueError(
            f"Invalid memory format: '{value}'. "
            "Expected format like 128m, 512m, 1g, 2g."
        )
    amount, unit = match.group(1), match.group(2).lower()
    # Ensure at least 4 MB (Docker minimum)
    bytes_val = float(amount) * _MEMORY_UNITS[unit]
    if bytes_val < 4 * 1024 * 1024:
        raise ValueError("Memory limit must be at least 4m (Docker minimum).")
    return f"{amount}{unit}"


# ── CPU ───────────────────────────────────────────────────────────────
def validate_cpus(value: float) -> float:
    """Validate CPU limit (0.1 – 16.0)."""
    if not 0.1 <= value <= 16.0:
        raise ValueError(
            f"Invalid CPU value: {value}. Must be between 0.1 and 16.0."
        )
    return value


# ── Timeout ───────────────────────────────────────────────────────────
def validate_timeout(value: int) -> int:
    """Validate timeout in seconds (1 – 3600)."""
    if not 1 <= value <= 3600:
        raise ValueError(
            f"Invalid timeout: {value}. Must be between 1 and 3600 seconds."
        )
    return value


# ── Script path ───────────────────────────────────────────────────────
def validate_script_path(value: str) -> Path:
    """Ensure the script file exists and is readable."""
    path = Path(value).resolve()
    if not path.exists():
        raise ValueError(f"Script not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    return path


# ── Language ──────────────────────────────────────────────────────────
def validate_language(value: str) -> str:
    """Validate that *value* is a supported language."""
    lang = value.lower().strip()
    aliases = {"js": "node", "javascript": "node", "sh": "bash", "shell": "bash"}
    lang = aliases.get(lang, lang)
    if lang not in SUPPORTED_LANGUAGES and lang not in {
        "python",
        "node",
        "bash",
        "ruby",
        "go",
        "perl",
    }:
        raise ValueError(
            f"Unsupported language: '{value}'. "
            f"Supported: {', '.join(SUPPORTED_LANGUAGES)}"
        )
    return lang
