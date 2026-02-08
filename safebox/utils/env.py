"""Environment variable parsing utilities.

Stub for Phase 3 — full --env / --env-file support.
"""

from __future__ import annotations

from pathlib import Path


def parse_env_pair(pair: str) -> tuple[str, str]:
    """Parse a ``KEY=VALUE`` string into a (key, value) tuple."""
    if "=" not in pair:
        raise ValueError(f"Invalid env format: '{pair}'. Expected KEY=VALUE.")
    key, _, value = pair.partition("=")
    key = key.strip()
    if not key:
        raise ValueError("Environment variable name cannot be empty.")
    return key, value


def load_env_file(path: str | Path) -> dict[str, str]:
    """Load environment variables from a .env-style file."""
    env: dict[str, str] = {}
    filepath = Path(path)
    if not filepath.is_file():
        raise FileNotFoundError(f"Env file not found: {filepath}")

    for lineno, raw_line in enumerate(filepath.read_text().splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(
                f"Bad format at {filepath}:{lineno} — expected KEY=VALUE."
            )
        key, _, value = line.partition("=")
        # Strip optional quotes around value
        value = value.strip().strip("\"'")
        env[key.strip()] = value

    return env
