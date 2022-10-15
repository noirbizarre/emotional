from __future__ import annotations

from dataclasses import dataclass
from random import randbytes

import pytest

from commitizen.git import GitCommit
from commitizen.config import BaseConfig

from emotional.config import EmotionalConfig, EmotionalSettings


@dataclass
class Factory:
    config: EmotionalConfig

    def parsed_message(self, **kwargs) -> tuple[dict, GitCommit]:
        parsed = {"type": "chore", "scope": None, "message": "I am a message", **kwargs}
        prefix = parsed["type"]
        msg = [f'{prefix}: {parsed["message"]}']
        if (body := parsed.get("body")) is not None:
            msg.extend(("", body))
        if (footers := parsed.get("footers")) is not None:
            msg.extend(("", footers))
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
    # config.settings.update({"name": "emotional"})
    config.settings.update(settings)
    # for marker in request.node.iter_markers("settings"):
    #     config.settings.update(marker.kwargs)
    return config


@pytest.fixture
def shiny_config(settings) -> EmotionalConfig:
    return EmotionalConfig(settings)


@pytest.fixture
def factory(shiny_config: EmotionalConfig) -> Factory:
    return Factory(shiny_config)
