## 🚀 v1.2.0 (2019-04-19)

### 💫 New features

- custom cz plugins now support bumping version

### 📖 Documentation

- how to create custom bumps
- added bump gif

## 🚀 v1.1.1 (2019-04-18)

### 🚨 Breaking changes

- changed stdout statements
- I broke something
- **commit**: moved most of the commit logic to the commit command

### 🐛 Bug fixes

- **bump**: commit message now fits better with semver
- conventional commit 'breaking change' in body instead of title

### 📖 Documentation

- **README**: updated documentation url
- mkdocs documentation

### 🔧 Refactorings

- **schema**: command logic removed from commitizen base
- **info**: command logic removed from commitizen base
- **example**: command logic removed from commitizen base

## 🚀 v1.1.0 (2019-04-14)

### 💫 New features

- new working bump command
- create version tag
- update given files with new version
- **config**: new set key, used to set version to cfg
- support for pyproject.toml
- **config**: can group by scope
- first semantic version bump implementation

### 🐛 Bug fixes

- removed all from commit
- fix config file not working

### 📖 Documentation

- **README**: some new information about bump
- **README**: ensure type aliases works
- added new changelog

### 🔧 Refactorings

- added commands folder, better integration with decli

## 🚀 v1.0.0 (2019-03-01)

### 🚨 Breaking changes

- API is stable

### 📖 Documentation

- **README**: new badges
- updated test command

### 🔧 Refactorings

- removed delegator, added decli and many tests

## 🚀 1.0.0b2 (2019-01-18)

### 📖 Documentation

- **README**: updated to reflect current state

## 🚀 v1.0.0b1 (2019-01-17)

### 💫 New features

- py3 only, tests and conventional commits 1.0

## 🚀 v0.9.11 (2018-12-17)

### 🐛 Bug fixes

- **config**: load config reads in order without failing if there is no commitizen section

## 🚀 v0.9.10 (2018-09-22)

### 🐛 Bug fixes

- parse scope (this is my punishment for not having tests)

## 🚀 v0.9.9 (2018-09-22)

### 🐛 Bug fixes

- parse scope empty

## 🚀 v0.9.8 (2018-09-22)

### 🐛 Bug fixes

- **scope**: parse correctly again

## 🚀 v0.9.7 (2018-09-22)

### 🐛 Bug fixes

- **scope**: parse correctly

## 🚀 v0.9.6 (2018-09-19)

### 🐛 Bug fixes

- **manifest**: included missing files

### 🔧 Refactorings

- **conventionalCommit**: moved filters to questions instead of message

## 🚀 v0.9.5 (2018-08-24)

### 🐛 Bug fixes

- **config**: home path for python versions between 3.0 and 3.5

## 🚀 v0.9.4 (2018-08-02)

### 💫 New features

- **cli**: added version

## 🚀 v0.9.3 (2018-07-28)

### 💫 New features

- **committer**: conventional commit is a bit more intelligent now

### 📖 Documentation

- **README**: motivation

## 🚀 v0.9.2 (2017-11-11)

### 🔧 Refactorings

- renamed conventional_changelog to conventional_commits, not backward compatible

## 🚀 v0.9.1 (2017-11-11)

### 🐛 Bug fixes

- **setup.py**: future is now required for every python version
