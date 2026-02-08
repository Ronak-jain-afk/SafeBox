"""Detect language from shebang (#!) line."""

from __future__ import annotations

import re
from pathlib import Path

from safebox.config.constants import SHEBANG_MAP, SHEBANG_READ_SIZE

_SHEBANG_RE = re.compile(
    r"^#!\s*(?:/usr/bin/env\s+(?:-\S+\s+)*)?"
    r"(?:/[^\s]*/)*"
    r"([a-zA-Z_][a-zA-Z0-9_.-]*)",
)


def detect_by_shebang(script_path: Path) -> str | None:
    """Read the first line of *script_path* and try to match its shebang.

    Returns the canonical language name, or ``None`` if no shebang or
    unrecognised interpreter.
    """
    try:
        raw = script_path.read_bytes()[:SHEBANG_READ_SIZE]
    except (OSError, PermissionError):
        return None

    first_line = raw.split(b"\n", 1)[0].decode("utf-8", errors="replace").strip()

    if not first_line.startswith("#!"):
        return None

    match = _SHEBANG_RE.match(first_line)
    if not match:
        return None

    interpreter = match.group(1).lower()

    base = re.sub(r"[\d.]+$", "", interpreter)
    if not base:
        base = interpreter

    return SHEBANG_MAP.get(base) or SHEBANG_MAP.get(interpreter)
