"""Execution orchestrator — detect → configure → run → stream → report."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

from safebox.config.constants import (
    DEFAULT_CPUS,
    DEFAULT_MEMORY,
    DEFAULT_PIDS_LIMIT,
    DEFAULT_TIMEOUT,
    LANGUAGE_IMAGE_MAP,
)
from safebox.core.container import ContainerConfig, build_container_kwargs
from safebox.core.docker_client import ensure_image, get_client
from safebox.core.timeout import ExecutionTimeoutError, wait_with_timeout
from safebox.detection.detector import DetectionError, detect_language
from safebox.output.console import console
from safebox.output.display import (
    print_detection_info,
    print_error,
    print_execution_header,
    print_result,
)


@dataclass
class ExecutionResult:
    """Outcome of a sandboxed script run."""

    exit_code: int
    duration: float
    timed_out: bool = False
    output: str = ""
    language: str = ""
    image: str = ""


class ExecutionError(Exception):
    """Generic execution-level error."""


def execute(
    script_path: Path,
    *,
    language: str | None = None,
    memory: str = DEFAULT_MEMORY,
    cpus: float = DEFAULT_CPUS,
    timeout: int = DEFAULT_TIMEOUT,
    pids_limit: int = DEFAULT_PIDS_LIMIT,
    remove: bool = True,
    extra_args: str = "",
    environment: dict[str, str] | None = None,
) -> ExecutionResult:
    """Full execution pipeline for a single script.

    1. Detect language
    2. Resolve Docker image
    3. Pull image if necessary
    4. Build container configuration
    5. Create & start container
    6. Stream output
    7. Wait (with timeout)
    8. Collect result & clean up
    """

    try:
        lang = detect_language(script_path, language_override=language)
    except DetectionError as exc:
        print_error(str(exc))
        raise ExecutionError(str(exc)) from exc

    image = LANGUAGE_IMAGE_MAP.get(lang)
    if image is None:
        msg = (
            f"No default image for language '{lang}'. "
            "Use --image to specify one explicitly."
        )
        print_error(msg)
        raise ExecutionError(msg)

    print_detection_info(lang, image, script_path.name)

    ensure_image(image)

    config = ContainerConfig(
        image=image,
        language=lang,
        script_path=script_path,
        memory=memory,
        cpus=cpus,
        timeout=timeout,
        pids_limit=pids_limit,
        remove=remove,
        extra_args=extra_args,
        environment=environment or {},
    )

    print_execution_header(config)

    client = get_client()
    kwargs = build_container_kwargs(config)

    container = client.containers.run(**kwargs)
    start_time = time.monotonic()

    output_chunks: list[str] = []
    try:
        for chunk in container.logs(stream=True, follow=True):
            text = chunk.decode("utf-8", errors="replace")
            console.print(text, end="", highlight=False)
            output_chunks.append(text)
    except Exception:
        pass

    timed_out = False
    exit_code = 1

    try:
        wait_result = wait_with_timeout(container, timeout)
        exit_code = wait_result.get("StatusCode", 1)
    except ExecutionTimeoutError:
        timed_out = True
        exit_code = 124

    duration = time.monotonic() - start_time

    if remove and not timed_out:
        try:
            container.remove(force=True)
        except Exception:
            pass

    result = ExecutionResult(
        exit_code=exit_code,
        duration=duration,
        timed_out=timed_out,
        output="".join(output_chunks),
        language=lang,
        image=image,
    )

    print_result(result)
    return result
