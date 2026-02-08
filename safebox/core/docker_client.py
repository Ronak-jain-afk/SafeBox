"""Docker client wrapper — connection, health check, image management."""

from __future__ import annotations

from typing import TYPE_CHECKING

import docker
from docker.errors import DockerException, ImageNotFound

from safebox.output.console import console

if TYPE_CHECKING:
    from docker import DockerClient
    from docker.models.images import Image


class DockerNotAvailableError(Exception):
    """Raised when the Docker daemon is not reachable."""


_client: DockerClient | None = None


def get_client() -> DockerClient:
    """Return a cached :class:`docker.DockerClient`.

    Creates the client on first call.  Raises
    :class:`DockerNotAvailableError` with a user-friendly message if
    Docker is unreachable.
    """
    global _client
    if _client is not None:
        return _client

    try:
        _client = docker.from_env()
        _client.ping()
    except DockerException as exc:
        raise DockerNotAvailableError(
            "Could not connect to the Docker daemon. "
            "Make sure Docker Desktop is running.\n"
            f"  ↳ {exc}"
        ) from exc

    return _client


def ensure_image(image: str, *, pull: bool = False) -> Image:
    """Make sure *image* is available locally.

    Pulls the image with a Rich status spinner when it is missing
    (or when *pull* is ``True``).
    """
    import warnings

    warnings.filterwarnings("ignore", message=".*docker-credential.*")

    client = get_client()

    if not pull:
        try:
            return client.images.get(image)
        except ImageNotFound:
            pass

    with console.status(f"[bold cyan]Pulling image [yellow]{image}[/]…"):
        try:
            img = client.images.pull(image)
        except DockerException as exc:
            raise ImagePullError(
                f"Failed to pull image '{image}': {exc}\n"
                "  Tip: Check your internet connection and Docker login."
            ) from exc

    console.print(f"  [green]✓[/] Image [yellow]{image}[/] ready")
    return img


class ImagePullError(Exception):
    """Raised when an image cannot be pulled."""
