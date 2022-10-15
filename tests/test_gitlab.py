from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from emotional import gitlab

if TYPE_CHECKING:
    from tests.conftest import Factory


REPOSITORY = "emotional/test"

pytestmark = [pytest.mark.settings(gitlab=REPOSITORY)]


@pytest.fixture(
    params=[
        pytest.param("https://gitlab.com", id="default"),
        pytest.param(
            "https://my.company.com",
            marks=pytest.mark.settings(gitlab=f"https://my.company.com/{REPOSITORY}"),
            id="hosted",
        ),
    ]
)
def server(request):
    return request.param


def test_linkify_issue_in_message(factory: Factory, server: str):
    message = "Fixes #42"
    msg, commit = factory.parsed_message(type="fix", message=message)

    result = gitlab.changelog_message_hook(factory.config, msg, commit)

    assert result["message"] == f"Fixes [#42]({server}/{REPOSITORY}/issues/42)"


def test_linkify_multiple_issues_in_message(factory: Factory, server: str):
    message = "Fixes #42, #51 and #77"
    msg, commit = factory.parsed_message(type="fix", message=message)

    result = gitlab.changelog_message_hook(factory.config, msg, commit)

    assert result["message"] == (
        f"Fixes [#42]({server}/{REPOSITORY}/issues/42), "
        f"[#51]({server}/{REPOSITORY}/issues/51) "
        f"and [#77]({server}/{REPOSITORY}/issues/77)"
    )


def test_linkify_issue_in_scope(factory: Factory, server: str):
    msg, commit = factory.parsed_message(scope="#42", message="whatever")

    result = gitlab.changelog_message_hook(factory.config, msg, commit)

    assert result["scope"] == f"[#42]({server}/{REPOSITORY}/issues/42)"


def test_append_body_issue_link_to_message(factory: Factory, server: str):
    body = "Fixes #42"
    msg, commit = factory.parsed_message(type="fix", body=body)

    result = gitlab.changelog_message_hook(factory.config, msg, commit)

    assert result["message"].endswith(f" [#42]({server}/{REPOSITORY}/issues/42)")


def test_append_footer_issue_link_to_message(factory: Factory, server: str):
    footers = "Fixes: #42"
    msg, commit = factory.parsed_message(
        type="fix", message="message", body="body", footers=footers
    )

    result = gitlab.changelog_message_hook(factory.config, msg, commit)

    assert result["message"] == f"message [#42]({server}/{REPOSITORY}/issues/42)"


@pytest.mark.settings(gitlab=None)
def test_is_noop_with_configuration(factory: Factory):
    message = "Fixes #42"
    msg, commit = factory.parsed_message(type="fix", message=message)

    result = gitlab.changelog_message_hook(factory.config, msg, commit)

    assert result["message"] == message
