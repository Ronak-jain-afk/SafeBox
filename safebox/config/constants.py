"""Constants and default configuration values for SafeBox."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Language → default Docker image
# ---------------------------------------------------------------------------
LANGUAGE_IMAGE_MAP: dict[str, str] = {
    "python": "python:3.12-slim",
    "node": "node:20-slim",
    "javascript": "node:20-slim",
    "bash": "bash:5",
    "shell": "bash:5",
    "sh": "bash:5",
    "ruby": "ruby:3.3-slim",
    "go": "golang:1.22-slim",
    "perl": "perl:5.38-slim",
}

# ---------------------------------------------------------------------------
# File extension → canonical language name
# ---------------------------------------------------------------------------
EXTENSION_MAP: dict[str, str] = {
    ".py": "python",
    ".pyw": "python",
    ".js": "node",
    ".mjs": "node",
    ".cjs": "node",
    ".ts": "node",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".rb": "ruby",
    ".go": "go",
    ".pl": "perl",
    ".pm": "perl",
}

# ---------------------------------------------------------------------------
# Shebang interpreter patterns → canonical language name
# ---------------------------------------------------------------------------
SHEBANG_MAP: dict[str, str] = {
    "python": "python",
    "python3": "python",
    "python2": "python",
    "node": "node",
    "nodejs": "node",
    "bash": "bash",
    "sh": "bash",
    "zsh": "bash",
    "ruby": "ruby",
    "go": "go",
    "perl": "perl",
}

# ---------------------------------------------------------------------------
# Language → container entrypoint command
# ---------------------------------------------------------------------------
ENTRYPOINT_MAP: dict[str, str] = {
    "python": "python",
    "node": "node",
    "bash": "bash",
    "ruby": "ruby",
    "go": "go run",
    "perl": "perl",
}

# ---------------------------------------------------------------------------
# Resource defaults (Phase 1)
# ---------------------------------------------------------------------------
DEFAULT_MEMORY = "256m"
DEFAULT_CPUS = 1.0
DEFAULT_TIMEOUT = 60  # seconds
DEFAULT_PIDS_LIMIT = 64

# ---------------------------------------------------------------------------
# Container sandbox paths
# ---------------------------------------------------------------------------
SANDBOX_DIR = "/sandbox"
SANDBOX_SCRIPT_PATH = "/sandbox/script"

# ---------------------------------------------------------------------------
# Docker labels for SafeBox-managed containers
# ---------------------------------------------------------------------------
SAFEBOX_LABEL = "safebox"
SAFEBOX_LABEL_VALUE = "true"

# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
SHEBANG_READ_SIZE = 512  # bytes to read for shebang detection
SUPPORTED_LANGUAGES = sorted(set(EXTENSION_MAP.values()))
