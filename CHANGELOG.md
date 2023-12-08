## 🚀 0.4.1 (2023-12-08)

### 🐛 Bug fixes

- **changelog**: ensure rendered changelog is compatible with `pre-commit` `end-of-file-fixer`

### 📦 Build

- **version**: use a simpler way to fetch version from `VERSION`

<!-- End of file -->

## 🚀 0.4.0 (2023-10-23)

### 🚨 Breaking changes

- Requires `commitizen >= 0.12`

### 💫 New features

- **bump**: support bumpimg with `major_version_zero`

### 📦 Build

- **commitizen**: upgrade to `commitizen >= 0.12` changelog template handling
- **python**: drop Python 3.7 support


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

- **defaults**: ensure default types don't have duplicate shortcuts
- **type_map**: ensure type aliases are properly matched
- **changelog_pattern**: do not match conventional commit pattern outside the first line (merge commits)


## 🚀 0.1.0 (2023-05-26)

### 💫 New features

- **entrypoint**: expose both v2 and v3 commitizen format
- **changelog**: add `group_by_scope` setting allowing to sort scope first
- **config**: support private github and gitlab instances
- initial import, works with test coverage

### 🐛 Bug fixes

- **readme**: tix typo in README

### 📦 Build

- **CHANGELOG**: use commitizen scm provider
- update linting stack
- drop support for Commitizen < 3.0
- **python**: support Python 3.11
- **pre-commit**: update to latest pre-commit plugins versions
- **pyproject**: add cz_emotional module for commitizen
- **pre-commit**: update pre-commit hooks
- **pyproject**: update dependencies

###  

- **README**: add integrations documentation

