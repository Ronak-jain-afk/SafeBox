"""Main detection orchestrator — determines script language/runtime."""

from __future__ import annotations

from pathlib import Path

from safebox.detection.extension import detect_by_extension
from safebox.detection.shebang import detect_by_shebang


class DetectionError(Exception):
    """Raised when the language of a script cannot be determined."""


def detect_language(
    script_path: Path,
    *,
    language_override: str | None = None,
) -> str:
    """Determine the language for *script_path*.

    Resolution order:
        1. Explicit ``--language`` override (``language_override``)
        2. File extension
        3. Shebang line

    Raises :class:`DetectionError` if none of the strategies succeed.
    """
    if language_override:
        lang = language_override.lower().strip()
        aliases = {"js": "node", "javascript": "node", "sh": "bash", "shell": "bash"}
        return aliases.get(lang, lang)

    lang = detect_by_extension(script_path)
    if lang:
        return lang

    lang = detect_by_shebang(script_path)
    if lang:
        return lang

    raise DetectionError(
        f"Cannot detect language for '{script_path.name}'. "
        "Use --language to specify it explicitly."
    )
