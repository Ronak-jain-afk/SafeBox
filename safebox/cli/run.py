"""``safebox run`` command — execute a script inside a sandboxed container."""

from __future__ import annotations

from typing import Optional

import typer

from safebox.config.constants import DEFAULT_CPUS, DEFAULT_MEMORY, DEFAULT_PIDS_LIMIT, DEFAULT_TIMEOUT
from safebox.core.executor import ExecutionError, execute
from safebox.output.display import print_error
from safebox.utils.files import resolve_script
from safebox.utils.validators import validate_cpus, validate_memory, validate_timeout


def run(
    script: str = typer.Argument(
        ...,
        help="Path to the script file to execute.",
    ),
    language: Optional[str] = typer.Option(
        None,
        "--language",
        "-l",
        help="Force language/runtime (python, node, bash, ruby, go).",
    ),
    memory: str = typer.Option(
        DEFAULT_MEMORY,
        "--memory",
        "-m",
        help="Memory limit (e.g. 256m, 1g).",
    ),
    cpus: float = typer.Option(
        DEFAULT_CPUS,
        "--cpus",
        help="CPU limit (e.g. 0.5, 1.0, 2.0).",
    ),
    timeout: int = typer.Option(
        DEFAULT_TIMEOUT,
        "--timeout",
        "-t",
        help="Kill execution after N seconds.",
    ),
    pids_limit: int = typer.Option(
        DEFAULT_PIDS_LIMIT,
        "--pids-limit",
        help="Max number of processes inside the container.",
    ),
    rm: bool = typer.Option(
        True,
        "--rm/--keep",
        help="Remove container after execution (default: remove).",
    ),
) -> None:
    """Run a script inside a sandboxed Docker container.

    SafeBox auto-detects the language from the file extension or shebang,
    selects the appropriate Docker image, applies resource limits, and
    streams the output in real time.

    \b
    Examples:
        safebox run hello.py
        safebox run --memory 512m --timeout 30 server.js
        safebox run -l bash script_no_extension
    """
    try:
        script_path = resolve_script(script)
    except FileNotFoundError as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc

    try:
        memory = validate_memory(memory)
        cpus = validate_cpus(cpus)
        timeout = validate_timeout(timeout)
    except ValueError as exc:
        print_error(str(exc))
        raise typer.Exit(code=1) from exc

    try:
        result = execute(
            script_path,
            language=language,
            memory=memory,
            cpus=cpus,
            timeout=timeout,
            pids_limit=pids_limit,
            remove=rm,
        )
    except ExecutionError:
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        print_error("Interrupted by user.")
        raise typer.Exit(code=130)
    except Exception as exc:
        print_error(f"Unexpected error: {exc}")
        raise typer.Exit(code=1) from exc

    raise typer.Exit(code=result.exit_code)
