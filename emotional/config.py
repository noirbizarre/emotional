from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field, fields
from functools import total_ordering

from commitizen.config import read_cfg
from commitizen.defaults import Settings

from ._compat import Literal, cached_property  # type: ignore
from .defaults import TYPES

RE_HTTP = re.compile(r"(?P<server>https?://.+)/(?P<repository>[^/]+/[^/]+/?)")


@dataclass
@total_ordering
class CommitType:
    type: str
    """Key used as type in the commit header"""

    description: str
    """A human readable description of the type"""

    heading: str | None
    """The resulting heading in the changelog for this type"""

    emoji: str | None
    """An optional emoji repsenting the type"""

    aliases: list[str] = field(default_factory=list)
    """Some known alternative keys (for legacy, typos...)"""

    changelog: bool = True
    """Wether this type should appear in the changelog or not"""

    question: bool = True
    """Wether this type should appear in the question choices"""

    bump: Literal["MAJOR", "MINOR", "PATCH"] = "PATCH"

    key: str | None = None

    def __str__(self) -> str:
        return self.type

    def __hash__(self):
        return hash(self.type)

    def __eq__(self, other):
        if isinstance(other, CommitType):
            return self.type.lower() == other.type.lower()
        elif isinstance(other, str):
            return self.type.lower() == other.lower()

    def __lt__(self, other):
        if isinstance(other, CommitType):
            return self.type.lower() < other.type.lower()
        elif isinstance(other, str):
            return self.type.lower() < other.lower()

    @property
    def shortcut(self) -> str:
        return self.key or self.type[0]

    @classmethod
    def from_dict(cls, data: dict) -> CommitType:
        fieldset = {f.name for f in fields(cls) if f.init}
        filtered = {k: v for k, v in data.items() if k in fieldset}
        return cls(**filtered)

    @classmethod
    def from_list(cls, lst: list[dict]) -> list[CommitType]:
        return [cls.from_dict(d) for d in lst]


class EmotionalSettings(Settings):
    types: list[dict] | None
    """The list of accepted types"""

    extra_types: list[dict] | None
    """A list of additional types (permit addition without loosing defaults)"""

    github: str | None

    gitlab: str | None

    jira_url: str | None
    jira_prefixes: list[str] | None

    release_type: str
    """
    If set to an existing type, this type will be ignored except for the release commit
    and it body will serve as introduction (using markdown)
    """


@dataclass
class EmotionalConfig:
    settings: EmotionalSettings = field(default_factory=lambda: read_cfg().settings)

    @property
    def types(self) -> list[CommitType]:
        return CommitType.from_list(self.settings.get("types", TYPES))

    @property
    def extra_types(self) -> list[CommitType]:
        return CommitType.from_list(self.settings.get("extra_types", []))

    @cached_property
    def known_types(self) -> list[CommitType]:
        return self.types + self.extra_types

    @cached_property
    def github(self) -> str | None:
        repository = self.settings.get("github")
        if not repository:
            return None
        match = RE_HTTP.match(repository)
        return match.group("repository") if match else repository

    @cached_property
    def github_url(self) -> str:
        repository = self.settings.get("github")
        if repository:
            match = RE_HTTP.match(repository)
            if match:
                return match.group("server")
        return "https://github.com"

    @cached_property
    def gitlab(self) -> str | None:
        repository = self.settings.get("gitlab")
        if not repository:
            return None
        match = RE_HTTP.match(repository)
        return match.group("repository") if match else repository

    @cached_property
    def gitlab_url(self) -> str:
        repository = self.settings.get("gitlab")
        if repository:
            match = RE_HTTP.match(repository)
            if match:
                return match.group("server")
        return "https://gitlab.com"

    @cached_property
    def jira_url(self) -> str | None:
        return self.settings.get("jira_url")

    @cached_property
    def jira_prefixes(self) -> list[str]:
        return self.settings.get("jira_prefixes", [])

    @property
    def incremental(self) -> bool:
        return "--incremental" in sys.argv
