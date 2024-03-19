from __future__ import annotations

RELEASE_EMOJI = "🚀"

TYPES: list[dict] = [
    dict(
        type="BREAKING CHANGE",
        description="Changes that are not backward-compatibles",
        heading="Breaking changes",
        emoji="🚨",
        bump="MAJOR",
        regex=r"BREAKING[\-\ ]CHANGE",
        question=False,  # Breaking changes have a dedicated question
    ),
    dict(
        type="feat",
        description="A new feature",
        heading="New features",
        emoji="💫",
        bump="MINOR",
        key="n",
    ),
    dict(
        type="fix",
        description="A bug fix",
        heading="Bug fixes",
        emoji="🐛",
        bump="PATCH",
    ),
    dict(
        type="perf",
        description="A changeset improving performance",
        heading="Performance",
        emoji="📈",
        aliases=["performance"],
        bump="PATCH",
    ),
    dict(
        type="docs",
        description="Documentation only change",
        heading="Documentation",
        emoji="📖",
        aliases=["doc"],
    ),
    dict(
        type="build",
        description=(
            "Changes that affect the build system or external dependencies (ex: pip, docker, npm)"
        ),
        heading="Build",
        emoji="📦",
        aliases=["deps"],
    ),
    dict(
        type="style",
        description=(
            "Changes that do not affect the meaning of the code (white-space, formatting, …)"
        ),
        heading="Style",
        emoji="🎨",
        changelog=False,
    ),
    dict(
        type="test",
        description="Adding missing or correcting existing tests",
        heading="Testing",
        emoji="🚦",
        aliases=["tests"],
        changelog=False,
    ),
    dict(
        type="ci",
        description="Changes to CI configuration files and scripts",
        heading="Continuous Integration",
        emoji="🛸",
        changelog=False,
    ),
    dict(
        type="refactor",
        description="A changeset neither fixing a bug nor adding a feature",
        heading="Refactorings",
        emoji="🔧",
        changelog=False,
        bump="PATCH",
    ),
    dict(
        type="i18n",
        description="A changeset related to languages and translations",
        heading="Internationalization",
        emoji="🌍",
        aliases=["locales", "l10n"],
        bump="PATCH",
    ),
    dict(
        type="chore",
        description="Changes not fitting in other categories",
        heading="Chores",
        emoji="🧹",
        key="o",
    ),
    dict(
        type="revert",
        description="Revert one or more commits",
        heading="Reverted",
        emoji="🔙",
        changelog=False,
        key="e",
    ),
    dict(
        type="wip",
        description="Work in progress",
        heading="Work in progress",
        emoji="🚧",
        changelog=False,
    ),
    dict(
        type="bump",
        description="A bump commit",
        heading="",
        emoji=RELEASE_EMOJI,
        aliases=["release"],
        changelog=False,
        question=False,
    ),
]
