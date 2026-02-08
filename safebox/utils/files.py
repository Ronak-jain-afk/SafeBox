"""File system utilities."""

from __future__ import annotations

from pathlib import Path


def resolve_script(script: str) -> Path:
    """Resolve *script* to an absolute :class:`Path`, raising on missing."""
    path = Path(script).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Script not found: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    return path
