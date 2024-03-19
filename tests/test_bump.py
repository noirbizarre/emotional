from __future__ import annotations

import pytest

from commitizen import bump
from commitizen.git import GitCommit

from emotional.plugin import Emotional

NONE_INCREMENT = [
    "docs(README): motivation",
    "ci: added travis",
    "performance. Remove or disable the reimplemented linters",
    "refactor that how this line starts",
]

PATCH_INCREMENTS = [
    "fix(setup.py): future is now required for every python version",
    "docs(README): motivation",
]

MINOR_INCREMENTS = [
    "feat(cli): added version",
    "docs(README): motivation",
    "fix(setup.py): future is now required for every python version",
    "perf: app is much faster",
    "refactor: app is much faster",
]

MAJOR_INCREMENTS_BREAKING_CHANGE = [
    "feat(cli): added version",
    "docs(README): motivation",
    "BREAKING CHANGE: `extends` key in config file is now used for extending other config files",  # noqa
    "fix(setup.py): future is now required for every python version",
]

MAJOR_INCREMENTS_BREAKING_CHANGE_ALT = [
    "feat(cli): added version",
    "docs(README): motivation",
    "BREAKING-CHANGE: `extends` key in config file is now used for extending other config files",  # noqa
    "fix(setup.py): future is now required for every python version",
]

MAJOR_INCREMENTS_EXCLAMATION = [
    "feat(cli)!: added version",
    "docs(README): motivation",
    "fix(setup.py): future is now required for every python version",
]

MAJOR_INCREMENTS_EXCLAMATION_SAMPLE_2 = ["feat(pipeline)!: some text with breaking change"]

MAJOR_INCREMENTS_EXCLAMATION_OTHER_TYPE = [
    "chore!: drop support for Python 3.9",
    "docs(README): motivation",
    "fix(setup.py): future is now required for every python version",
]


@pytest.mark.parametrize(
    "messages, expected_type",
    (
        (PATCH_INCREMENTS, "PATCH"),
        (MINOR_INCREMENTS, "MINOR"),
        (MAJOR_INCREMENTS_BREAKING_CHANGE, "MAJOR"),
        (MAJOR_INCREMENTS_BREAKING_CHANGE_ALT, "MAJOR"),
        (MAJOR_INCREMENTS_EXCLAMATION_OTHER_TYPE, "MAJOR"),
        (MAJOR_INCREMENTS_EXCLAMATION, "MAJOR"),
        (MAJOR_INCREMENTS_EXCLAMATION_SAMPLE_2, "MAJOR"),
        (NONE_INCREMENT, None),
    ),
)
def test_find_increment(messages, expected_type, config):
    cz = Emotional(config)
    commits = [GitCommit(rev="test", title=message) for message in messages]
    increment_type = bump.find_increment(
        commits,
        regex=cz.bump_pattern,
        increments_map=cz.bump_map,
    )
    assert increment_type == expected_type


@pytest.mark.parametrize(
    "messages, expected_type",
    (
        (PATCH_INCREMENTS, "PATCH"),
        (MINOR_INCREMENTS, "MINOR"),
        (MAJOR_INCREMENTS_BREAKING_CHANGE, "MINOR"),
        (MAJOR_INCREMENTS_BREAKING_CHANGE_ALT, "MINOR"),
        (MAJOR_INCREMENTS_EXCLAMATION_OTHER_TYPE, "MINOR"),
        (MAJOR_INCREMENTS_EXCLAMATION, "MINOR"),
        (MAJOR_INCREMENTS_EXCLAMATION_SAMPLE_2, "MINOR"),
        (NONE_INCREMENT, None),
    ),
)
def test_find_increment_major_version_zero(messages, expected_type, config):
    cz = Emotional(config)
    commits = [GitCommit(rev="test", title=message) for message in messages]
    increment_type = bump.find_increment(
        commits,
        regex=cz.bump_pattern,
        increments_map=cz.bump_map_major_version_zero,
    )
    assert increment_type == expected_type
