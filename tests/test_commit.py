from __future__ import annotations

import re

from typing import Any, TypedDict, cast

import pytest

from commitizen.commands.check import Check
from commitizen.cz.exceptions import AnswerRequiredError

from emotional.plugin import Emotional, parse_scope, parse_subject

valid_scopes = ["", "simple", "dash-separated", "camelCase", "UPPERCASE"]

scopes_transformations = [["with spaces", "with-spaces"], [None, ""]]

valid_subjects = ["this is a normal text", "aword"]

subjects_transformations = [["with dot.", "with dot"]]

invalid_subjects = ["", "   ", ".", "   .", "", None]


def test_parse_scope_valid_values():
    for valid_scope in valid_scopes:
        assert valid_scope == parse_scope(valid_scope)


def test_scopes_transformations():
    for scopes_transformation in scopes_transformations:
        invalid_scope, transformed_scope = scopes_transformation
        assert transformed_scope == parse_scope(invalid_scope)


def test_parse_subject_valid_values():
    for valid_subject in valid_subjects:
        assert valid_subject == parse_subject(valid_subject)


def test_parse_subject_invalid_values():
    for valid_subject in invalid_subjects:
        with pytest.raises(AnswerRequiredError):
            parse_subject(valid_subject)


def test_subject_transformations():
    for subject_transformation in subjects_transformations:
        invalid_subject, transformed_subject = subject_transformation
        assert transformed_subject == parse_subject(invalid_subject)


def test_questions(config):
    emotional = Emotional(config)
    questions = emotional.questions()
    assert isinstance(questions, list)
    assert isinstance(questions[0], dict)


def test_choices_all_have_keyboard_shortcuts(config):
    emotional = Emotional(config)
    questions = emotional.questions()

    list_questions = (q for q in questions if q["type"] == "list")
    for select in list_questions:
        assert all("key" in choice for choice in select["choices"])


def test_choices_dont_have_duplicate_keyboard_shortcuts(config):
    emotional = Emotional(config)
    questions = emotional.questions()

    list_questions = (q for q in questions if q["type"] == "list")
    for select in list_questions:
        shortcuts = [choice.get("key") for choice in select["choices"]]
        assert len(set(shortcuts)) == len(shortcuts)


def test_small_answer(config):
    emotional = Emotional(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "is_breaking_change": False,
        "body": "",
        "footer": "",
    }
    message = emotional.message(answers)
    assert message == "fix(users): email pattern corrected"


def test_no_scope(config):
    emotional = Emotional(config)
    answers = {
        "prefix": "fix",
        "scope": "",
        "subject": "email pattern corrected",
        "is_breaking_change": False,
        "body": "",
        "footer": "",
    }
    message = emotional.message(answers)
    assert message == "fix: email pattern corrected"


def test_long_answer(config):
    emotional = Emotional(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "is_breaking_change": False,
        "body": "complete content",
        "footer": "closes #24",
    }
    message = emotional.message(answers)
    assert message == (
        "fix(users): email pattern corrected\n\ncomplete content\n\ncloses #24"  # noqa
    )


def test_breaking_change_in_footer(config):
    emotional = Emotional(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "body": "complete content",
        "is_breaking_change": True,
        "breaking_change": "breaking change content",
        "footer": "Fixes #42",
    }
    message = emotional.message(answers)
    assert message == (
        "fix(users): email pattern corrected\n"
        "\n"
        "complete content\n"
        "\n"
        "BREAKING CHANGE: breaking change content\n"
        "Fixes #42"
    )


def test_exclamation_mark_breaking_change(config):
    emotional = Emotional(config)
    answers = {
        "prefix": "fix",
        "scope": "users",
        "subject": "email pattern corrected",
        "body": "complete content",
        "is_breaking_change": True,
        "breaking_change": "",
        "footer": "Fixes #42",
    }
    message = emotional.message(answers)
    assert message == ("fix(users)!: email pattern corrected\n\ncomplete content\n\nFixes #42")


def test_exclamation_mark_breaking_change_without_scope(config):
    emotional = Emotional(config)
    answers = {
        "prefix": "fix",
        "scope": "",
        "subject": "email pattern corrected",
        "body": "complete content",
        "is_breaking_change": True,
        "breaking_change": "",
        "footer": "Fixes #42",
    }
    message = emotional.message(answers)
    assert message == ("fix!: email pattern corrected\n\ncomplete content\n\nFixes #42")


@pytest.mark.parametrize(
    "message",
    [
        "bump: version 0.0.0 → 0.1.0",
        "bump: version 0.1.0 → 0.1.1",
        "bump: version 1.0.0 → 1.1.0",
    ],
)
def test_validate_bump_commit(config, message: str):
    emotional = Emotional(config)
    check = Check(config, {"message": message})
    pattern = re.compile(emotional.schema_pattern())
    check._validate_commit_message(message, pattern, "")


class ParsedCommit(TypedDict):
    change_type: str
    message: str
    emoji: str | None
    scope: str | None
    breaking: str | None
    body: str | None
    footer: str | None


def commit(change_type: str, message: str, **kwargs) -> ParsedCommit:
    params: dict[str, Any] = {k: kwargs.get(k) for k in ParsedCommit.__annotations__}
    params["change_type"] = change_type
    params["message"] = message
    return cast(ParsedCommit, params)


PARSED_COMMITS = (
    ("fix: something", commit("fix", "something")),
    ("fix(scope): something", commit("fix", "something", scope="scope")),
    ("bump: version 1.1.1 → 1.2.0", commit("bump", "version 1.1.1 → 1.2.0")),
)


@pytest.mark.parametrize("message,expected", PARSED_COMMITS)
def test_commit_parser(config, message, expected):
    emotional = Emotional(config)
    parser = re.compile(emotional.commit_parser, re.MULTILINE)
    parsed = parser.match(message)
    assert parsed, f"Unparsed commit: {message}"
    assert ParsedCommit(**parsed.groupdict()) == expected
