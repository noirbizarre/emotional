"""
See:
    - https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically
    - https://docs.gitlab.com/ee/user/markdown.html#gitlab-specific-references
"""

from __future__ import annotations

import re

from commitizen.git import GitCommit

from .config import EmotionalConfig

RE_ISSUE = re.compile(r"(?P<repository>(?P<owner>\w+)/(?P<project>\w+))?#(?P<issue>\d+)")

RE_ISSUE_URL = r"{config.gitlab_url}/(?P<owner>\w+)/(?P<project>\w+)/issues/(?P<issue>\d+)"
RE_CLOSING_PATTERN = (
    r"\b((?:"
    r"[Cc]los(?:e[sd]?|ing)"
    r"|\b[Ff]ix(?:e[sd]|ing)?"
    r"|\b[Rr]esolv(?:e[sd]?|ing)"
    r"|\b[Ii]mplement(?:s|ed|ing)?"
    r")(:?)"
    r"\s+"
    r"(?:"
    r"(?:issues? +)"
    r"?%{issue_ref}"
    r"(?:(?: *,? +and +| *,? *)?)|([A-Z][A-Z0-9_]+-\d+))+)"
)


def changelog_message_hook(
    config: EmotionalConfig, parsed_message: dict, commit: GitCommit
) -> dict:
    if config.gitlab is None:
        return parsed_message

    def urlize_issue(match: re.Match[str]) -> str:
        repository = match.group("repository") or config.gitlab
        label = match.group(0)
        issue = match.group("issue")
        return f"[{label}]({config.gitlab_url}/{repository}/issues/{issue})"

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
