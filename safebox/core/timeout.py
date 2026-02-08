"""Timeout handling for container execution."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from safebox.output.console import console

if TYPE_CHECKING:
    from docker.models.containers import Container


class ExecutionTimeoutError(Exception):
    """Raised when a container exceeds its allowed execution time."""


def wait_with_timeout(container: Container, timeout: int) -> dict:
    """Block until *container* exits **or** *timeout* seconds elapse.

    Returns the Docker wait-result dict ``{"StatusCode": N}`` on success.
    Raises :class:`ExecutionTimeoutError` if the timeout fires (the
    container is killed and removed as a side-effect).
    """
    result: dict | None = None
    error: Exception | None = None

    def _wait() -> None:
        nonlocal result, error
        try:
            result = container.wait()
        except Exception as exc:  # noqa: BLE001
            error = exc

    thread = threading.Thread(target=_wait, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    if thread.is_alive():
        # Timeout expired — kill the container
        console.print(
            f"\n[bold red]⏱  Timeout![/] Container exceeded {timeout}s limit — killing…"
        )
        try:
            container.kill()
        except Exception:  # noqa: BLE001
            pass  # container may have already exited
        try:
            container.remove(force=True)
        except Exception:  # noqa: BLE001
            pass
        raise ExecutionTimeoutError(
            f"Script execution timed out after {timeout} seconds."
        )

    if error is not None:
        raise error  # propagate unexpected Docker errors

    return result  # type: ignore[return-value]
