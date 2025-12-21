from __future__ import annotations

from dataclasses import dataclass
from random import getrandbits

import pytest

from commitizen.config import BaseConfig
from commitizen.git import GitCommit

from emotional.config import EmotionalConfig, EmotionalSettings


def randbytes(size: int) -> bytes:
    return bytearray(getrandbits(8) for _ in range(size))


@dataclass
class Factory:
    config: EmotionalConfig

    def parsed_message(self, **kwargs) -> tuple[dict, GitCommit]:
        parsed = {"type": "chore", "scope": None, "message": "I am a message", **kwargs}
        prefix = parsed["type"]
        msg = [f"{prefix}: {parsed['message']}"]
        body = parsed.get("body")
        if body is not None:
            msg.extend(("", body))
        footer = parsed.get("footer")
        if footer is not None:
            msg.extend(("", footer))
        return parsed, self.commit("\n".join(msg))

    def commit(self, title: str, **kwargs) -> GitCommit:
        return GitCommit(rev=str(randbytes(8)), title=title, **kwargs)


@pytest.fixture
def settings(request) -> EmotionalSettings:
    settings = EmotionalSettings()
    for marker in reversed(list(request.node.iter_markers("settings"))):
        settings.update(marker.kwargs)
    return settings


@pytest.fixture
def config(settings):
    config = BaseConfig()
    config.settings.update({"name": "emotional"})
    config.settings.update(settings)
    return config


@pytest.fixture
def emotional_config(settings) -> EmotionalConfig:
    return EmotionalConfig(settings)


@pytest.fixture
def factory(emotional_config: EmotionalConfig) -> Factory:
    return Factory(emotional_config)
