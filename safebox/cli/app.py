"""SafeBox CLI — main Typer application and entry point."""

from __future__ import annotations

from typing import Optional

import typer

from safebox import __version__
from safebox.output.logger import setup_logging

app = typer.Typer(
    name="safebox",
    help="🔒 SafeBox — Docker-based script sandboxing made easy.",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def _version_callback(value: bool) -> None:  # noqa: FBT001
    if value:
        typer.echo(f"safebox {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging."),
    version: Optional[bool] = typer.Option(  # noqa: UP007
        None,
        "--version",
        "-V",
        help="Show version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """Global options processed before any subcommand."""
    setup_logging(verbose=verbose)


# ── Register subcommands ──────────────────────────────────────────────
# Import here to avoid circular imports and ensure registration
from safebox.cli.run import run  # noqa: E402, F401

app.command()(run)


# Allow ``python -m safebox`` to work
if __name__ == "__main__":
    app()
