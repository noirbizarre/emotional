"""
See:
    - https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
    - https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls#issues-and-pull-requests
"""  # noqa: E501

from __future__ import annotations

import re

from commitizen.git import GitCommit

from .config import EmotionalConfig

RE_ISSUE = re.compile(r"(?P<repository>(?P<owner>\w+)/(?P<project>\w+))?#(?P<issue>\d+)")

KEYWORDS = (
    "close",
    "closes",
    "closed",
    "fix",
    "fixes",
    "fixed",
    "resolve",
    "resolves",
    "resolved",
)


def changelog_message_hook(
    config: EmotionalConfig, parsed_message: dict, commit: GitCommit
) -> dict:
    if config.github is None:
        return parsed_message

    def urlize_issue(match: re.Match[str]) -> str:
        label = match.group(0)
        repository = match.group("repository") or config.github
        issue = match.group("issue")
        return f"[{label}]({config.github_url}/{repository}/issues/{issue})"

    for field in "message", "scope":
        value = parsed_message[field]
        if value:
            parsed_message[field] = RE_ISSUE.sub(urlize_issue, value)

    for field in "body", "footers":
        body = parsed_message.get(field)
        if body:
            for match in RE_ISSUE.finditer(body):
                parsed_message["message"] += f" {urlize_issue(match)}"

    return parsed_message
