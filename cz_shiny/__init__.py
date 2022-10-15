from ._version import __version__  # noqa: F401
from .changelog import monkeypatch
from .cz import CzShiny

discover_this = CzShiny

monkeypatch()
