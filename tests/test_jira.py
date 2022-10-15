from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from emotional import jira

if TYPE_CHECKING:
    from tests.conftest import Factory


REPOSITORY = "emotional/test"

JIRA_URL = "https://company.atlassian.com"

pytestmark = [pytest.mark.settings(jira_url=JIRA_URL, jira_prefixes=["TEST-", "EMO-"])]


def test_linkify_issue_in_message(factory: Factory):
    message = "Fixes TEST-42"
    msg, commit = factory.parsed_message(type="fix", message=message)

    result = jira.changelog_message_hook(factory.config, msg, commit)

    assert result["message"] == f"Fixes [TEST-42]({JIRA_URL}/browse/TEST-42)"


def test_linkify_multiple_issues_in_message(factory: Factory):
    message = "Fixes TEST-42, TEST-51, UNKNOWN-1 and EMO-1"
    msg, commit = factory.parsed_message(type="fix", message=message)

    result = jira.changelog_message_hook(factory.config, msg, commit)

    assert result["message"] == (
        f"Fixes [TEST-42]({JIRA_URL}/browse/TEST-42), "
        f"[TEST-51]({JIRA_URL}/browse/TEST-51), "
        "UNKNOWN-1 "
        f"and [EMO-1]({JIRA_URL}/browse/EMO-1)"
    )


def test_linkify_issue_in_scope(factory: Factory):
    msg, commit = factory.parsed_message(scope="TEST-42", message="whatever")

    result = jira.changelog_message_hook(factory.config, msg, commit)

    assert result["scope"] == f"[TEST-42]({JIRA_URL}/browse/TEST-42)"


def test_append_body_issue_link_to_message(factory: Factory):
    body = "Fixes TEST-42"
    msg, commit = factory.parsed_message(type="fix", body=body)

    result = jira.changelog_message_hook(factory.config, msg, commit)

    assert result["message"].endswith(f" [TEST-42]({JIRA_URL}/browse/TEST-42)")


@pytest.mark.parametrize(
    "footers",
    (
        pytest.param("Fixes: TEST-42", id="git-trail-fix"),
        pytest.param("TEST-42", id="jira-id-only"),
        pytest.param("Fixes: TEST-42\nFixes: #51", id="mixed"),
    ),
)
def test_append_footer_issue_link_to_message(factory: Factory, footers: str):
    msg, commit = factory.parsed_message(
        type="fix", message="message", body="body", footers=footers
    )

    result = jira.changelog_message_hook(factory.config, msg, commit)

    assert result["message"] == f"message [TEST-42]({JIRA_URL}/browse/TEST-42)"


@pytest.mark.settings(jira_url=None)
def test_is_noop_with_configuration(factory: Factory):
    message = "Fixes TEST-42"
    msg, commit = factory.parsed_message(type="fix", message=message)

    result = jira.changelog_message_hook(factory.config, msg, commit)

    assert result["message"] == message
