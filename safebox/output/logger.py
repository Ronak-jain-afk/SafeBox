"""Structured logging with Rich handler.

Stub for Phase 4 polish — provides basic logging setup.
"""

from __future__ import annotations

import logging

from rich.logging import RichHandler

from safebox.output.console import console


def setup_logging(*, verbose: bool = False) -> None:
    """Configure root logger with a Rich handler."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )
