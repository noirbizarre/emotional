## 🚀 0.6.0 (2025-12-28)

### 🚨 Breaking changes

- update the stack and target `commitizen>=4.0`

### 📖 Documentation

- **readme**: update the badges to use codecov


## 🚀 0.5.1 (2024-03-26)

### 🐛 Bug fixes

- **changelog**: generated changelog pass `pre-commit` `end-of-file-fixer` by default

### 📦 Build

- update the stack


## 🚀 0.5.0 (2024-03-11)

### 🚨 Breaking changes

- `emotional` now requires `commitizen>=3.18`

### 🐛 Bug fixes

- **breaking-changes**: Breaking changes are now visible
- **changelog**: ensure consistent changelog end of file without a marker

## 🚀 0.4.1 (2023-12-08)

### 🐛 Bug fixes

- **changelog**: ensure rendered changelog is compatible with `pre-commit` `end-of-file-fixer`

### 📦 Build

- **version**: use a simpler way to fetch version from `VERSION`

## 🚀 0.4.0 (2023-10-23)

### 🚨 Breaking changes

- **python**: drop Python 3.7 support
- Requires `commitizen >= 0.12`

### 💫 New features

- **bump**: support bumpimg with `major_version_zero`

### 📦 Build

- **commitizen**: upgrade to `commitizen >= 0.12` changelog template handling

## 🚀 0.3.2 (2023-06-16)

### 🐛 Bug fixes

- **bump**: restore the hidden `bump` type validating bump commits

## 🚀 0.3.1 (2023-06-16)

### 🐛 Bug fixes

- **changelog**: ensure produced changelog is compliant with standard pre-commit trimming rule

## 🚀 0.3.0 (2023-05-30)

### 💫 New features

- **changelog**: add `order_by_scope` options to group changes with the same scope first

## 🚀 0.2.1 (2023-05-28)

### 🐛 Bug fixes

- **pyproject**: fix scm project version and build backend

## 🚀 0.2.0 (2023-05-28)

### 💫 New features

- **bump**: support bump increment detection
- **releases**: the release heading emoji can be set with `release_emoji`

### 🐛 Bug fixes

- **changelog_pattern**: do not match conventional commit pattern outside the first line (merge commits)
- **defaults**: ensure default types don't have duplicate shortcuts
- **type_map**: ensure type aliases are properly matched

## 🚀 0.1.0 (2023-05-26)

### 🚨 Breaking changes

- drop support for Commitizen < 3.0

### 💫 New features

- **changelog**: add `group_by_scope` setting allowing to sort scope first
- **config**: support private github and gitlab instances
- **entrypoint**: expose both v2 and v3 commitizen format
- initial import, works with test coverage

### 🐛 Bug fixes

- **readme**: tix typo in README

### 📖 Documentation

- **README**: add integrations documentation

### 📦 Build

- **CHANGELOG**: use commitizen scm provider
- **pre-commit**: update to latest pre-commit plugins versions
- **pre-commit**: update pre-commit hooks
- **pyproject**: add cz_emotional module for commitizen
- **pyproject**: update dependencies
- **python**: support Python 3.11
- update linting stack