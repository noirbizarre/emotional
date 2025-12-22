from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from commitizen import git
from commitizen.changelog import Metadata
from commitizen.commands.changelog import Changelog
from commitizen.exceptions import DryRunExit
from pytest_mock import MockerFixture
from syrupy.extensions.single_file import SingleFileSnapshotExtension, WriteMode

FIXTURES = Path(__file__).parent / "fixtures/changelogs"


class MarkdownSnapshotExtension(SingleFileSnapshotExtension):
    file_extension = "md"
    _write_mode = WriteMode.TEXT


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(MarkdownSnapshotExtension)


COMMITS_DATA = [
    {
        "rev": "141ee441c9c9da0809c554103a558eb17c30ed17",
        "title": "bump: version 1.1.1 → 1.2.0",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "6c4948501031b7d6405b54b21d3d635827f9421b",
        "title": "docs: how to create custom bumps",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "ddd220ad515502200fe2dde443614c1075d26238",
        "title": "feat: custom cz plugins now support bumping version",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "ad17acff2e3a2e141cbc3c6efd7705e4e6de9bfc",
        "title": "docs: added bump gif",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "56c8a8da84e42b526bcbe130bd194306f7c7e813",
        "title": "bump: version 1.1.0 → 1.1.1",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "74c6134b1b2e6bb8b07ed53410faabe99b204f36",
        "title": "refactor!: changed stdout statements",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "cbc7b5f22c4e74deff4bc92d14e19bd93524711e",
        "title": "fix(bump): commit message now fits better with semver",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "1ba46f2a63cb9d6e7472eaece21528c8cd28b118",
        "title": "fix: conventional commit 'breaking change' in body instead of title",
        "body": "closes #16",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "c35dbffd1bb98bb0b3d1593797e79d1c3366af8f",
        "title": "refactor(schema): command logic removed from commitizen base",
        "body": "BREAKING CHANGE: I broke something",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "25313397a4ac3dc5b5c986017bee2a614399509d",
        "title": "refactor(info): command logic removed from commitizen base",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "d2f13ac41b4e48995b3b619d931c82451886e6ff",
        "title": "refactor(example): command logic removed from commitizen base",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "d839e317e5b26671b010584ad8cc6bf362400fa1",
        "title": "refactor(commit)!: moved most of the commit logic to the commit command",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "12d0e65beda969f7983c444ceedc2a01584f4e08",
        "title": "docs(README): updated documentation url",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "fb4c85abe51c228e50773e424cbd885a8b6c610d",
        "title": "docs: mkdocs documentation",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "17efb44d2cd16f6621413691a543e467c7d2dda6",
        "title": "Bump version 1.0.0 → 1.1.0",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "6012d9eecfce8163d75c8fff179788e9ad5347da",
        "title": "test: fixed issues with conf",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "0c7fb0ca0168864dfc55d83c210da57771a18319",
        "title": "docs(README): some new information about bump",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "0c7fb0ca0168864dfc55d83c210da57771a18377",
        "title": "doc(README): ensure type aliases works",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "cb1dd2019d522644da5bdc2594dd6dee17122d7f",
        "title": "feat: new working bump command",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "9c7450f85df6bf6be508e79abf00855a30c3c73c",
        "title": "feat: create version tag",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "9f3af3772baab167e3fd8775d37f041440184251",
        "title": "docs: added new changelog",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "b0d6a3defbfde14e676e7eb34946409297d0221b",
        "title": "feat: update given files with new version",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "d630d07d912e420f0880551f3ac94e933f9d3beb",
        "title": "fix: removed all from commit",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "1792b8980c58787906dbe6836f93f31971b1ec77",
        "title": "Merge pull request #85 from whatever",
        "body": "feat(config): new set key, used to set version to cfg",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "1792b8980c58787906dbe6836f93f31971b1ec2d",
        "title": "feat(config): new set key, used to set version to cfg",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "52def1ea3555185ba4b936b463311949907e31ec",
        "title": "feat: support for pyproject.toml",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "1792b8980c58787906dbe6836f93f31971b1ec22",
        "title": "feat(config): can group by scope",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "3127e05077288a5e2b62893345590bf1096141b7",
        "title": "feat: first semantic version bump implementation",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "fd480ed90a80a6ffa540549408403d5b60d0e90c",
        "title": "fix: fix config file not working",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "e4840a059731c0bf488381ffc77e989e85dd81ad",
        "title": "refactor: added commands folder, better integration with decli",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "aa44a92d68014d0da98965c0c2cb8c07957d4362",
        "title": "Bump version: 1.0.0b2 → 1.0.0",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "58bb709765380dbd46b74ce6e8978515764eb955",
        "title": "docs(README): new badges",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "97afb0bb48e72b6feca793091a8a23c706693257",
        "title": "Merge pull request #10 from Woile/feat/decli",
        "body": "Feat/decli",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "9cecb9224aa7fa68d4afeac37eba2a25770ef251",
        "title": "style: black to files",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "f5781d1a2954d71c14ade2a6a1a95b91310b2577",
        "title": "ci: added travis",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "80105fb3c6d45369bc0cbf787bd329fba603864c",
        "title": "refactor: removed delegator, added decli and many tests",
        "body": "BREAKING CHANGE: API is stable",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "a96008496ffefb6b1dd9b251cb479eac6a0487f7",
        "title": "docs: updated test command",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "aab33d13110f26604fb786878856ec0b9e5fc32b",
        "title": "Bump version: 1.0.0b1 → 1.0.0b2",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "b73791563d2f218806786090fb49ef70faa51a3a",
        "title": "docs(README): updated to reflect current state",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "7aa06a454fb717408b3657faa590731fb4ab3719",
        "title": "Merge pull request #9 from Woile/dev",
        "body": "feat: py3 only, tests and conventional commits 1.0",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "7c7e96b723c2aaa1aec3a52561f680adf0b60e97",
        "title": "Bump version: 0.9.11 → 1.0.0b1",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "ed830019581c83ba633bfd734720e6758eca6061",
        "title": "feat: py3 only, tests and conventional commits 1.0",
        "body": "more tests\npyproject instead of Pipfile\nquestionary instead of whaaaaat (promptkit 2.0.0 support)",  # noqa: E501
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "c52eca6f74f844ab3ffbde61d98ef96071e132b7",
        "title": "Bump version: 0.9.10 → 0.9.11",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "0326652b2657083929507ee66d4d1a0899e861ba",
        "title": "fix(config): load config reads in order without failing if there is no commitizen section",  # noqa: E501
        "body": "Closes #8",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "b3f89892222340150e32631ae6b7aab65230036f",
        "title": "Bump version: 0.9.9 → 0.9.10",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "5e837bf8ef0735193597372cd2d85e31a8f715b9",
        "title": "fix: parse scope (this is my punishment for not having tests)",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "684e0259cc95c7c5e94854608cd3dcebbd53219e",
        "title": "Bump version: 0.9.8 → 0.9.9",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "ca38eac6ff09870851b5c76a6ff0a2a8e5ecda15",
        "title": "fix: parse scope empty",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "64168f18d4628718c49689ee16430549e96c5d4b",
        "title": "Bump version: 0.9.7 → 0.9.8",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "9d4def716ef235a1fa5ae61614366423fbc8256f",
        "title": "fix(scope): parse correctly again",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "33b0bf1a0a4dc60aac45ed47476d2e5473add09e",
        "title": "Bump version: 0.9.6 → 0.9.7",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "696885e891ec35775daeb5fec3ba2ab92c2629e1",
        "title": "fix(scope): parse correctly",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "bef4a86761a3bda309c962bae5d22ce9b57119e4",
        "title": "Bump version: 0.9.5 → 0.9.6",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "72472efb80f08ee3fd844660afa012c8cb256e4b",
        "title": "refactor(conventionalCommit): moved filters to questions instead of message",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "b5561ce0ab3b56bb87712c8f90bcf37cf2474f1b",
        "title": "fix(manifest): included missing files",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "3e31714dc737029d96898f412e4ecd2be1bcd0ce",
        "title": "Bump version: 0.9.4 → 0.9.5",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "9df721e06595fdd216884c36a28770438b4f4a39",
        "title": "fix(config): home path for python versions between 3.0 and 3.5",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "0cf6ada372470c8d09e6c9e68ebf94bbd5a1656f",
        "title": "Bump version: 0.9.3 → 0.9.4",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "973c6b3e100f6f69a3fe48bd8ee55c135b96c318",
        "title": "feat(cli): added version",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "dacc86159b260ee98eb5f57941c99ba731a01399",
        "title": "Bump version: 0.9.2 → 0.9.3",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "4368f3c3cbfd4a1ced339212230d854bc5bab496",
        "title": "feat(committer): conventional commit is a bit more intelligent now",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "da94133288727d35dae9b91866a25045038f2d38",
        "title": "docs(README): motivation",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "1541f54503d2e1cf39bd777c0ca5ab5eb78772ba",
        "title": "Bump version: 0.9.1 → 0.9.2",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "ddc855a637b7879108308b8dbd85a0fd27c7e0e7",
        "title": "refactor: renamed conventional_changelog to conventional_commits, not backward compatible",  # noqa: E501
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "46e9032e18a819e466618c7a014bcb0e9981af9e",
        "title": "Bump version: 0.9.0 → 0.9.1",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
    {
        "rev": "0fef73cd7dc77a25b82e197e7c1d3144a58c1350",
        "title": "fix(setup.py): future is now required for every python version",
        "body": "",
        "author": "Commitizen",
        "author_email": "author@cz.dev",
    },
]


TAGS = [
    ("v1.2.0", "141ee441c9c9da0809c554103a558eb17c30ed17", "2019-04-19"),
    ("v1.1.1", "56c8a8da84e42b526bcbe130bd194306f7c7e813", "2019-04-18"),
    ("v1.1.0", "17efb44d2cd16f6621413691a543e467c7d2dda6", "2019-04-14"),
    ("v1.0.0", "aa44a92d68014d0da98965c0c2cb8c07957d4362", "2019-03-01"),
    ("1.0.0b2", "aab33d13110f26604fb786878856ec0b9e5fc32b", "2019-01-18"),
    ("v1.0.0b1", "7c7e96b723c2aaa1aec3a52561f680adf0b60e97", "2019-01-17"),
    ("v0.9.11", "c52eca6f74f844ab3ffbde61d98ef96071e132b7", "2018-12-17"),
    ("v0.9.10", "b3f89892222340150e32631ae6b7aab65230036f", "2018-09-22"),
    ("v0.9.9", "684e0259cc95c7c5e94854608cd3dcebbd53219e", "2018-09-22"),
    ("v0.9.8", "64168f18d4628718c49689ee16430549e96c5d4b", "2018-09-22"),
    ("v0.9.7", "33b0bf1a0a4dc60aac45ed47476d2e5473add09e", "2018-09-22"),
    ("v0.9.6", "bef4a86761a3bda309c962bae5d22ce9b57119e4", "2018-09-19"),
    ("v0.9.5", "3e31714dc737029d96898f412e4ecd2be1bcd0ce", "2018-08-24"),
    ("v0.9.4", "0cf6ada372470c8d09e6c9e68ebf94bbd5a1656f", "2018-08-02"),
    ("v0.9.3", "dacc86159b260ee98eb5f57941c99ba731a01399", "2018-07-28"),
    ("v0.9.2", "1541f54503d2e1cf39bd777c0ca5ab5eb78772ba", "2017-11-11"),
    ("v0.9.1", "46e9032e18a819e466618c7a014bcb0e9981af9e", "2017-11-11"),
]


@pytest.fixture
def gitcommits() -> list[git.GitCommit]:
    return [git.GitCommit(**commit) for commit in COMMITS_DATA]


@pytest.fixture
def tags() -> list[git.GitTag]:
    tags = [git.GitTag(*tag) for tag in TAGS]
    return tags


@pytest.fixture(
    params=[
        pytest.param(False, id="full"),
        pytest.param(True, id="incremental"),
    ]
)
def incremental(request: pytest.FixtureRequest) -> bool:
    return cast(bool, request.param)


@pytest.fixture
def render_changelog(config, gitcommits, tags, capsys, mocker: MockerFixture, incremental: bool):
    """
    Generate a changelog using the same flow as the cz changelog command.
    """

    def fixture(unreleased: bool = True, **kwargs) -> str:
        mocker.patch(
            "commitizen.git.get_commits", return_value=gitcommits[:4] if incremental else gitcommits
        )
        mocker.patch("commitizen.git.get_tags", return_value=tags)
        kwargs["dry_run"] = True
        kwargs["incremental"] = incremental
        kwargs["unreleased_version"] = unreleased
        cmd = Changelog(config, kwargs)
        mocker.patch.object(cmd.changelog_format, "get_metadata").return_value = Metadata(
            latest_version="1.1.1"
        )
        capsys.readouterr()
        try:
            cmd()
        except DryRunExit:
            pass
        return capsys.readouterr().out

    return fixture


def test_render_changelog_with_default_settings(render_changelog, snapshot):
    assert render_changelog() == snapshot


@pytest.mark.settings(order_by_scope=True)
def test_render_changelog_order_by_scope(render_changelog, snapshot):
    assert render_changelog() == snapshot


@pytest.mark.settings(group_by_scope=True)
def test_render_changelog_group_by_scope(render_changelog, snapshot):
    assert render_changelog() == snapshot


@pytest.mark.settings(release_emoji="🎉")
def test_render_changelog_release_emoji(render_changelog, snapshot):
    assert render_changelog() == snapshot
