"""Rich display helpers — panels, tables, result banners."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.panel import Panel
from rich.table import Table

from safebox.output.console import console

if TYPE_CHECKING:
    from safebox.core.container import ContainerConfig
    from safebox.core.executor import ExecutionResult


def print_detection_info(language: str, image: str, script_name: str) -> None:
    """Print a compact panel showing the detected language and image."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()

    table.add_row("Script", f"[white]{script_name}[/]")
    table.add_row("Language", f"[yellow]{language}[/]")
    table.add_row("Image", f"[magenta]{image}[/]")

    console.print(Panel(table, title="[bold]🔍 Detection", border_style="blue", expand=False))


def print_execution_header(config: ContainerConfig) -> None:
    """Print a table of resource limits before execution starts."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()

    table.add_row("Memory", f"[white]{config.memory}[/]")
    table.add_row("CPUs", f"[white]{config.cpus}[/]")
    table.add_row("Timeout", f"[white]{config.timeout}s[/]")
    table.add_row("PIDs limit", f"[white]{config.pids_limit}[/]")
    table.add_row("Auto-remove", f"[white]{config.remove}[/]")

    console.print(Panel(table, title="[bold]⚙️  Resources", border_style="green", expand=False))
    console.print()


def print_result(result: ExecutionResult) -> None:
    """Print the final result banner."""
    console.print()

    if result.timed_out:
        console.print(
            Panel(
                f"[bold red]TIMED OUT[/] after [yellow]{result.duration:.1f}s[/]",
                title="[bold]⏱  Result",
                border_style="red",
                expand=False,
            )
        )
        return

    if result.exit_code == 0:
        status = "[bold green]PASSED[/]"
        border = "green"
        icon = "✅"
    else:
        status = f"[bold red]FAILED[/] (exit code {result.exit_code})"
        border = "red"
        icon = "❌"

    duration_str = f"[dim]{result.duration:.2f}s[/]"

    console.print(
        Panel(
            f"{status}  {duration_str}",
            title=f"[bold]{icon} Result",
            border_style=border,
            expand=False,
        )
    )


def print_error(message: str) -> None:
    """Print a styled error panel."""
    console.print(
        Panel(
            f"[bold red]{message}[/]",
            title="[bold]❌ Error",
            border_style="red",
            expand=False,
        )
    )


def print_info(message: str) -> None:
    """Print a styled info message."""
    console.print(f"  [cyan]ℹ[/]  {message}")
