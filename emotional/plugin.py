from __future__ import annotations

import itertools

from collections import OrderedDict
from collections.abc import Iterable
from typing import Any

from commitizen.config.base_config import BaseConfig
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.git import GitCommit
from jinja2 import PackageLoader

from . import github, gitlab, jira
from .config import CommitType, EmotionalConfig, Increment
from .utils import render_template

INTEGRATIONS = github, gitlab, jira

RE_EMOJI = (
    "["
    "\U0001f1e0-\U0001f1ff"  # flags (iOS)
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f680-\U0001f6ff"  # transport & map symbols
    "\U0001f700-\U0001f77f"  # alchemical symbols
    "\U0001f780-\U0001f7ff"  # Geometric Shapes Extended
    "\U0001f800-\U0001f8ff"  # Supplemental Arrows-C
    "\U0001f900-\U0001f9ff"  # Supplemental Symbols and Pictographs
    "\U0001fa00-\U0001fa6f"  # Chess Symbols
    "\U0001fa70-\U0001faff"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027b0"  # Dingbats
    "]"
)

BREAKING_CHANGE_TYPE = "BREAKING CHANGE"


def parse_scope(text):
    if not text:
        return ""

    scope = text.strip().split()
    if len(scope) == 1:
        return scope[0]

    return "-".join(scope)


def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="Subject is required.")


class Emotional(BaseCommitizen):
    template_loader = PackageLoader("emotional", "templates")

    def __init__(self, config: BaseConfig):
        super().__init__(config)
        self.emotional_config = EmotionalConfig(config.settings)

    @property
    def known_types(self) -> dict[str, CommitType]:
        return dict(
            itertools.chain(
                ((t.type, t) for t in self.emotional_config.known_types),
                (
                    (alias, t)
                    for t in self.emotional_config.known_types
                    for alias in t.aliases
                    if t.aliases
                ),
            )
        )

    @property
    def re_known_types(self) -> str:
        return "|".join(t.regex or k for k, t in self.known_types.items())

    @property
    def bump_pattern(self) -> str:
        """Regex to extract information from commit (subject and body)"""
        re_types = "|".join(t.regex or k for k, t in self.known_types.items() if t.bump)
        return rf"^((({re_types})(\(.+\))?(!)?)|\w+!):"

    @property
    def bump_map(self) -> dict[str, Increment]:
        """
        Mapping the extracted information to a SemVer increment type (MAJOR, MINOR, PATCH)
        """
        return OrderedDict(
            (
                (r"^.+!$", "MAJOR"),
                *((rf"^{t.regex or k}", t.bump) for k, t in self.known_types.items() if t.bump),
            )
        )

    @property
    def bump_map_major_version_zero(self) -> dict[str, Increment]:
        return OrderedDict(
            (pattern, increment.replace("MAJOR", "MINOR"))  # type:ignore[misc]
            for pattern, increment in self.bump_map.items()
        )  # ty:ignore[invalid-return-type]

    def questions(self) -> list:
        questions: list[dict[str, Any]] = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": t.type,
                        "name": f"{t.emoji} {t.type}: {t.description}",
                        "key": t.shortcut,
                    }
                    for t in self.emotional_config.known_types
                    if t.question
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "Scope. Define Could be anything specifying place of the "
                    "commit change (users, db, poll):\n"
                ),
                "filter": parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": parse_subject,
                "message": (
                    "Subject. Concise description of the changes. "
                    "Imperative, lower case and no period:\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Body. Motivation for the change and contrast this with previous behavior:\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE?",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "when": lambda x: x["is_breaking_change"],
                "type": "input",
                "name": "breaking_change",
                "message": "Breaking changes. Details the breakage:\n",
                "filter": multiple_line_breaker,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and "
                    "reference issues that this commit impacts:\n"
                ),
                "filter": multiple_line_breaker,
            },
        ]
        for integration in INTEGRATIONS:
            if hasattr(integration, "questions"):
                questions = integration.questions(self.emotional_config, questions)
        return questions

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        is_breaking_change = answers["is_breaking_change"]
        breaking_change = answers.get("breaking_change")
        footer = answers.get("footer", "")
        extra = ""

        if scope:
            scope = f"({scope})"

        if is_breaking_change and not breaking_change:
            scope += "!"

        if body:
            body = f"\n\n{body}"

        if is_breaking_change and breaking_change:
            footer = f"BREAKING CHANGE: {breaking_change}\n{footer}"

        if footer:
            footer = f"\n\n{footer}"

        message = f"{prefix}{scope}: {subject}{extra}{body}{footer}"

        return message

    def changelog_message_builder_hook(
        self, parsed_message: dict, commit: GitCommit
    ) -> dict[str, Any] | Iterable[dict[str, Any]] | None:
        """add github and jira links to the readme"""
        # Remap breaking changes type
        if parsed_message.get("breaking"):
            parsed_message["change_type"] = BREAKING_CHANGE_TYPE
        # Filter out changes not meant to appear in the changelog
        if (ct := self.known_types.get(parsed_message["change_type"])) and not ct.changelog:
            return None
        for integration in INTEGRATIONS:
            if hasattr(integration, "changelog_message_hook"):
                parsed_message = integration.changelog_message_hook(
                    self.emotional_config, parsed_message, commit
                )
        return parsed_message

    def changelog_hook(self, full: str, partial: str | None) -> str:
        """
        Process resulting changelog to keep 1 empty line at the end of file
        """
        changelog = partial or full
        return changelog.rstrip()

    @property
    def change_type_order(self) -> list[CommitType]:
        return [
            type for type in self.emotional_config.known_types if type.changelog and type.heading
        ]

    @property
    def changelog_pattern(self) -> str:
        re_known_types = "|".join(k for k, t in self.known_types.items())
        return rf"\A({re_known_types})(\(.+\))?(!)?"

    @property
    def commit_parser(self) -> str:
        return (
            rf"\A(?:(?P<emoji>{RE_EMOJI})\s*)?"
            rf"(?P<change_type>{self.re_known_types})"
            r"(?:\((?P<scope>[^()\r\n]*)\)|\()?"
            r"(?P<breaking>!)?:\s"
            r"(?P<message>.*)?"
            r"(?:\n{2,}(?P<body>.*))?"
            r"(?:\n{2,}(?P<footer>.*))?"
        )

    @property
    def change_type_map(self) -> dict[str, CommitType]:
        return self.known_types

    def info(self) -> str:
        return render_template("info.md.jinja", config=self.emotional_config)

    def example(self) -> str:
        return render_template("example.jinja", config=self.emotional_config)

    def schema(self) -> str:
        return (
            "<type>(<scope>): <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: <breaking changes>)*\n"
            "(<footers>)*"
        )

    def schema_pattern(self) -> str:
        PATTERN = (
            r"(?s)"  # To explicitly make . match new line
            rf"({self.re_known_types})"  # type
            r"(\(\S+\))?!?:"  # scope
            r"( [^\n\r]+)"  # subject
            r"((\n\n.*)|(\s*))?$"
        )
        return PATTERN

    @property
    def template_extras(self) -> dict[str, Any]:
        return {"config": self.emotional_config, "settings": self.emotional_config.settings}
