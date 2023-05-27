import pytest
from commitizen.cz.exceptions import AnswerRequiredError

from emotional.plugin import Emotional, parse_scope, parse_subject

valid_scopes = ["", "simple", "dash-separated", "camelCase" "UPPERCASE"]

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
        "fix(users): email pattern corrected\n" "\n" "complete content\n" "\n" "closes #24"  # noqa
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
    assert message == (
        "fix(users)!: email pattern corrected\n" "\n" "complete content\n" "\n" "Fixes #42"
    )


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
    assert message == ("fix!: email pattern corrected\n" "\n" "complete content\n" "\n" "Fixes #42")


# @pytest.mark.parametrize(
#     ("commit_message", "expected_message"),
#     [
#         (
#             "test(test_scope): this is test msg",
#             "this is test msg",
#         ),
#         (
#             "test(test_scope)!: this is test msg",
#             "this is test msg",
#         ),
#         (
#             "test!(test_scope): this is test msg",
#             "",
#         ),
#     ],
# )
# def test_process_commit(commit_message, expected_message, config):
#     emotional = CzShiny(config)
#     message = emotional.process_commit(commit_message)
#     assert message == expected_message
