"""Container configuration and Docker-kwargs builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from safebox.config.constants import (
    DEFAULT_CPUS,
    DEFAULT_MEMORY,
    DEFAULT_PIDS_LIMIT,
    DEFAULT_TIMEOUT,
    ENTRYPOINT_MAP,
    SAFEBOX_LABEL,
    SAFEBOX_LABEL_VALUE,
    SANDBOX_DIR,
)


@dataclass
class ContainerConfig:
    """All parameters needed to create a sandboxed container."""

    image: str
    language: str
    script_path: Path
    script_name: str = ""

    # Resource limits
    memory: str = DEFAULT_MEMORY
    cpus: float = DEFAULT_CPUS
    timeout: int = DEFAULT_TIMEOUT
    pids_limit: int = DEFAULT_PIDS_LIMIT

    # Lifecycle
    remove: bool = True

    # Environment (Phase 3 placeholders)
    environment: dict[str, str] = field(default_factory=dict)
    extra_args: str = ""

    def __post_init__(self) -> None:
        if not self.script_name:
            self.script_name = self.script_path.name


def build_container_kwargs(config: ContainerConfig) -> dict:
    """Translate a :class:`ContainerConfig` into kwargs for
    ``client.containers.run()``.
    """
    # Build the command to run inside the container
    entrypoint = ENTRYPOINT_MAP.get(config.language, config.language)
    script_dest = f"{SANDBOX_DIR}/{config.script_name}"
    command = f"{entrypoint} {script_dest}"
    if config.extra_args:
        command += f" {config.extra_args}"

    # CPU → nano_cpus (1 CPU = 1_000_000_000)
    nano_cpus = int(config.cpus * 1_000_000_000)

    # Host path for bind-mount (must be absolute and posix-compatible for
    # Docker Engine on Windows via Docker Desktop)
    host_script = str(config.script_path.resolve())

    kwargs: dict = {
        "image": config.image,
        "command": command,
        "detach": True,
        "stdout": True,
        "stderr": True,
        # Resource limits
        "mem_limit": config.memory,
        "nano_cpus": nano_cpus,
        "pids_limit": config.pids_limit,
        # Filesystem
        "volumes": {
            host_script: {
                "bind": script_dest,
                "mode": "ro",
            },
        },
        "working_dir": SANDBOX_DIR,
        # Labels for cleanup / identification
        "labels": {
            SAFEBOX_LABEL: SAFEBOX_LABEL_VALUE,
            "safebox.language": config.language,
            "safebox.script": config.script_name,
        },
    }

    # Environment variables
    if config.environment:
        kwargs["environment"] = config.environment

    # Auto-remove is handled manually after we capture logs / exit code,
    # so we do NOT set remove=True here — we'll call container.remove()
    # ourselves in the executor.

    return kwargs
