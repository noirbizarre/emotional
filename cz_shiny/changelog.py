from __future__ import annotations

from collections.abc import Iterable

from .config import ShinyConfig
from .utils import render_template

TEMPLATE = "changelog.md.jinja"


def render_changelog(tree: Iterable, config: ShinyConfig | None = None) -> str:
    config = config or ShinyConfig()
    changelog: str = render_template(TEMPLATE, tree=tree, config=config, settings=config.settings)
    return changelog


def monkeypatch():
    from commitizen import changelog

    changelog.render_changelog = render_changelog
