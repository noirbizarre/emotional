from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from emotional.config import EmotionalConfig

if TYPE_CHECKING:
    from _pytest.mark import ParameterSet


def param(id, url, repo, **settings) -> ParameterSet:
    return pytest.param(url, repo, marks=pytest.mark.settings(**settings), id=id)


@pytest.mark.parametrize(
    "url,repository",
    [
        param("repo", "https://github.com", "org/repo", github="org/repo"),
        param("url", "https://github.com", "org/repo", github="https://github.com/org/repo"),
        param("hosted", "https://private.com", "org/repo", github="https://private.com/org/repo"),
    ],
)
def test_config_github_repository(emotional_config: EmotionalConfig, url: str, repository: str):
    assert emotional_config.github == repository
    assert emotional_config.github_url == url


@pytest.mark.parametrize(
    "url,repository",
    [
        param("repo", "https://gitlab.com", "org/repo", gitlab="org/repo"),
        param("url", "https://gitlab.com", "org/repo", gitlab="https://gitlab.com/org/repo"),
        param("hosted", "https://private.com", "org/repo", gitlab="https://private.com/org/repo"),
    ],
)
def test_config_gitlab_repository(emotional_config: EmotionalConfig, url: str, repository: str):
    assert emotional_config.gitlab == repository
    assert emotional_config.gitlab_url == url
