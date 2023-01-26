"""
Commitizen <= 3.0 compatibility layer
"""
from emotional.changelog import monkeypatch
from emotional.cz import CzEmotional

discover_this = CzEmotional

monkeypatch()
