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


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"safebox {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging."),
    version: Optional[bool] = typer.Option(
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


from safebox.cli.run import run

app.command()(run)


if __name__ == "__main__":
    app()
