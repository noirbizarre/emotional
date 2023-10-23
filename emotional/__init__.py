from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # type: ignore[no-redef,import-not-found]


def read_version() -> str:
    try:
        return version("emotional")
    except (PackageNotFoundError, ImportError):
        version_file = files(__package__) / "VERSION"
        return version_file.read_text() if version_file.is_file() else "0.0.0.dev"


__version__ = read_version()
