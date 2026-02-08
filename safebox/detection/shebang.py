"""Detect language from shebang (#!) line."""

from __future__ import annotations

import re
from pathlib import Path

from safebox.config.constants import SHEBANG_MAP, SHEBANG_READ_SIZE

# Matches common shebang patterns:
#   #!/usr/bin/python3
#   #!/usr/bin/env python3
#   #!/usr/bin/env -S python3
_SHEBANG_RE = re.compile(
    r"^#!\s*(?:/usr/bin/env\s+(?:-\S+\s+)*)?"  # optional env prefix
    r"(?:/[^\s]*/)*"                              # optional path prefix
    r"([a-zA-Z_][a-zA-Z0-9_.-]*)",               # interpreter name
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

    # Only inspect the first line
    first_line = raw.split(b"\n", 1)[0].decode("utf-8", errors="replace").strip()

    if not first_line.startswith("#!"):
        return None

    match = _SHEBANG_RE.match(first_line)
    if not match:
        return None

    interpreter = match.group(1).lower()

    # Strip version suffixes:  python3.12 → python3, node20 → node
    base = re.sub(r"[\d.]+$", "", interpreter)
    if not base:
        base = interpreter

    return SHEBANG_MAP.get(base) or SHEBANG_MAP.get(interpreter)
