# emotional

[![CI](https://github.com/noirbizarre/emotional/actions/workflows/ci.yml/badge.svg)](https://github.com/noirbizarre/emotional/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/noirbizarre/emotional/main.svg)](https://results.pre-commit.ci/latest/github/noirbizarre/emotional/main)
[![codecov](https://codecov.io/gh/noirbizarre/emotional/graph/badge.svg?token=Iha48GODCy)](https://codecov.io/gh/noirbizarre/emotional)

A [Commitizen][commitizen] template for [conventional commit][conventional-commit] with emojis and integrations.

## Installation

```shell
pip install emotional
```

Then set `emotional` as the Commitizen template:

```toml
[tool.commitizen]
name = "emotional"
```

## Configuration

As a starter, remember that all [Commitizen configuration][commitizen-config]
is available.

### Changelog

By default, changes by types are kept in order of commit and ignore the scope for ordering.
You can however force scope to be sorted first by setting `order_by_scope`:

```toml
[tool.commitizen]
name = "emotional"
order_by_scope = true
```

You can also group changes into subsections by scope by setting `group_by_scope`:

```toml
[tool.commitizen]
name = "emotional"
group_by_scope = true
```

### Github integration

To enable [github](https://github.com) integration, just provide your github repository as `github` setting:

```toml
[tool.commitizen]
name = "emotional"
github = "author/repository"
```

For github enterprise, you can use the full repository URL:

```toml
[tool.commitizen]
name = "emotional"
github = "https://git.company.com/author/repository"
```

### Gitlab integration

To enable [gitlab](https://gitlab.com) integration, just provide your gitlab repository as `gitlab` setting:

```toml
[tool.commitizen]
name = "emotional"
gitlab = "author/repository"
```

Use the full URL for hosted gitlab instances:

```toml
[tool.commitizen]
name = "emotional"
gitlab = "https://git.company.com/author/repository"
```

### Jira integration

To enable [Jira](https://www.atlassian.com/fr/software/jira) integration,
provide your JIRA instance URL as `jira_url` setting
and the list of project prefix you want ho be processed in `jira_prefixes`:

```toml
[tool.commitizen]
name = "emotional"
jira_url = "https://emotional.atlassian.net"
jira_prefixes = [
  "EMO-",
  "PRJ-",
]
```

### Multiple integrations

While it is totally possible to mix integrations,
keep in mind than `jira` is compatible with both `github` and `gitlab`
while `github` and `gitlab` are conflicting because they use the same format.


[commitizen]: https://commitizen-tools.github.io/commitizen/
[commitizen-config]: https://commitizen-tools.github.io/commitizen/config/
[conventional-commit]: https://www.conventionalcommits.org/
