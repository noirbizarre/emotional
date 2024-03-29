from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def read_version() -> str:
    try:
        return version("emotional")
    except (PackageNotFoundError, ImportError):
        version_file = Path(__file__).parent / "VERSION"
        return version_file.read_text() if version_file.is_file() else "0.0.0.dev"


__version__ = read_version()
