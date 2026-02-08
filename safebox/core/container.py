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

    memory: str = DEFAULT_MEMORY
    cpus: float = DEFAULT_CPUS
    timeout: int = DEFAULT_TIMEOUT
    pids_limit: int = DEFAULT_PIDS_LIMIT

    remove: bool = True

    environment: dict[str, str] = field(default_factory=dict)
    extra_args: str = ""

    def __post_init__(self) -> None:
        if not self.script_name:
            self.script_name = self.script_path.name


def build_container_kwargs(config: ContainerConfig) -> dict:
    """Translate a :class:`ContainerConfig` into kwargs for
    ``client.containers.run()``.
    """
    entrypoint = ENTRYPOINT_MAP.get(config.language, config.language)
    script_dest = f"{SANDBOX_DIR}/{config.script_name}"
    command = f"{entrypoint} {script_dest}"
    if config.extra_args:
        command += f" {config.extra_args}"

    nano_cpus = int(config.cpus * 1_000_000_000)

    host_script = str(config.script_path.resolve())

    kwargs: dict = {
        "image": config.image,
        "command": command,
        "detach": True,
        "stdout": True,
        "stderr": True,
        "mem_limit": config.memory,
        "nano_cpus": nano_cpus,
        "pids_limit": config.pids_limit,
        "volumes": {
            host_script: {
                "bind": script_dest,
                "mode": "ro",
            },
        },
        "working_dir": SANDBOX_DIR,
        "labels": {
            SAFEBOX_LABEL: SAFEBOX_LABEL_VALUE,
            "safebox.language": config.language,
            "safebox.script": config.script_name,
        },
    }

    if config.environment:
        kwargs["environment"] = config.environment

    return kwargs
