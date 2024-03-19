"""
See:
    - https://support.atlassian.com/jira-software-cloud/docs/process-issues-with-smart-commits/
    - https://confluence.atlassian.com/fisheye/using-smart-commits-960155400.html
"""

from __future__ import annotations

import re

from commitizen.git import GitCommit

from .config import EmotionalConfig


def changelog_message_hook(
    config: EmotionalConfig, parsed_message: dict, commit: GitCommit
) -> dict:
    if not config.jira_url or not config.jira_prefixes:
        return parsed_message

    prefixes = "|".join(config.jira_prefixes)
    re_issue = re.compile(rf"({prefixes})\d+")

    def urlize_issue(match: re.Match[str]) -> str:
        issue = match.group(0)
        return f"[{issue}]({config.jira_url}/browse/{issue})"

    for field in "message", "scope":
        value = parsed_message[field]
        if value:
            parsed_message[field] = re_issue.sub(urlize_issue, value)

    for field in "body", "footers":
        body = parsed_message.get(field)
        if body:
            for match in re_issue.finditer(body):
                parsed_message["message"] += f" {urlize_issue(match)}"

    return parsed_message
