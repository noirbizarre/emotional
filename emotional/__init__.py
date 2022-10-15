from ._version import __version__  # noqa: F401
from .changelog import monkeypatch
from .cz import CzEmotional

discover_this = CzEmotional

monkeypatch()
