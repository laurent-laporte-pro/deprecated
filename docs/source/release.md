(release)=

# Release process

This page explains how to prepare, document and publish a new release of Deprecated.

The project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html),
and its changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Overview

- The version is defined **only** in {file}`src/deprecated/__init__.py` (`__version__`).
  Hatch reads it to build the distributions (`[tool.hatch.version]` in {file}`pyproject.toml`),
  and it is updated with `hatch version <major|minor|patch>`.
  The Sphinx documentation reads it from the installed distribution metadata.
- The `develop` branch receives the pull requests; the `master` branch contains the releases.
- A release is prepared on a `release/X.Y.Z` branch (or `hotfix/X.Y.Z` for a patch
  of the latest release), merged into `master` with a pull request, then merged back
  into `develop`.
- The git tag `vX.Y.Z` is **not** created locally: it is created by GitHub when the release
  is published (see {ref}`release-publish`).

```{list-table} Which part of the version to bump?
:header-rows: 1
:widths: 15 85

* - Bump
  - When
* - `major`
  - Incompatible changes: removed or changed public API, dropped Python version...
* - `minor`
  - New backward-compatible features, new deprecations.
* - `patch`
  - Backward-compatible bug fixes only.
```

## 1. Prepare the release

Start from an up-to-date `develop` branch (or `master` for a hotfix):

```sh
git switch develop
git pull
git switch -c release/X.Y.Z      # or: git switch -c hotfix/X.Y.Z master
```

Bump the version:

```sh
hatch version            # show the current version, e.g.: 3.0.0
hatch version minor      # updates src/deprecated/__init__.py, e.g.: 3.0.0 => 3.1.0
```

:::{note}
`hatch version` refuses to lower the version: to fix a wrong bump, edit
`__version__` in {file}`src/deprecated/__init__.py` (or discard the change with git).
:::

The `make bump-major`, `make bump-minor` and `make bump-patch` targets are shortcuts
for these commands; `make version` shows the current version.

Then run `uv sync --reinstall-package deprecated`: the documentation reads the version
from the installed package metadata, which is not refreshed by `hatch version`.

Update the files which quote the version and cannot read it from the package metadata:

- {file}`python-deprecated.spec`: the `Version:` field (Packit updates the Fedora packages
  from the release, but the spec file of this repository must stay consistent);
- {file}`docs/source/_static/logo.svg`: the `vX.Y.Z` text (element `id="deprecated-version"`)
  of the logo, shown in the README and on the home page of the documentation. The text is
  right-aligned and fits up to 10 characters (e.g. `v10.10.100`).

Add a new section at the top of {file}`CHANGELOG.md` for the new version, marked as unreleased:

```markdown
## vX.Y.Z (unreleased)

Minor release: <one-line summary>

### Added

- ...
```

Commit these changes:

```sh
git add src/deprecated/__init__.py python-deprecated.spec CHANGELOG.md \
    docs/source/_static/logo.svg
git commit -m "chore: prepare release X.Y.Z"
```

## 2. Update the changelog from the pull requests

List the pull requests merged since the previous release `vA.B.C`, for instance with the
[GitHub CLI](https://cli.github.com/) (use the date of the previous release):

```sh
gh pr list --repo laurent-laporte-pro/deprecated --base develop --state merged \
    --search "merged:>=YYYY-MM-DD" --limit 200 \
    --json number,title,author --template \
    '{{range .}}- {{.title}} (#{{.number}}, @{{.author.login}}){{"\n"}}{{end}}'
```

or with git, from the merge commits:

```sh
git log --merges --first-parent --oneline vA.B.C..develop
```

The *compare* view of GitHub (`https://github.com/laurent-laporte-pro/deprecated/compare/vA.B.C...develop`)
gives the same information.

For each user-visible change, add an entry in the right category of the new section
(`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`, `Documentation`
or `Other`), and reference the pull request and its author:

```markdown
### Fixed

- Fix the stack level of the warnings of nested deprecated classes. See PR #123 (username).
```

Guidelines:

- write for the users of the library: describe the effect of the change, not its implementation;
- group the purely internal changes (CI, refactoring, tooling) in `Other`;
- write the changelog in plain Markdown, so that GitHub renders it too: standard links,
  no MyST roles, and GitHub alerts (`> [!WARNING]`) for the admonitions;
- flag the breaking changes with a `> [!WARNING]` alert at the top of the section;
- add the `.. versionadded::`, `.. versionchanged::` or `.. deprecated::` directives
  to the docstrings of the changed features, with the new version number.

## 3. Finalize the release

Replace `(unreleased)` by the release date (ISO 8601 format) in {file}`CHANGELOG.md`:

```markdown
## vX.Y.Z (YYYY-MM-DD)
```

Run the checks and build the documentation and the distributions:

```sh
make check        # uv lock --check + hatch check code/fmt/types
make test-all     # all Python and wrapt versions
make docs-check   # warnings are errors, like the CI
make build        # dist/deprecated-X.Y.Z.tar.gz and dist/deprecated-X.Y.Z-py3-none-any.whl
```

Commit, push the branch and open a pull request to `master`:

```sh
git commit -am "chore: release X.Y.Z"
git push -u origin release/X.Y.Z
```

The CI must be green before merging. Name the pull request `vX.Y.Z`.

(release-publish)=

## 4. Publish the release

Once the pull request is merged into `master`:

1. On GitHub, open *Releases* > *Draft a new release*.
2. In *Choose a tag*, type `vX.Y.Z` and select *Create new tag: vX.Y.Z on publish*;
   the target branch is `master`.
3. Use `vX.Y.Z` as the title, and copy the changelog section of the release in the description
   (the *Generate release notes* button lists the merged pull requests, useful to cross-check).
4. Click *Publish release*: GitHub creates the tag, and Packit proposes the update of the
   Fedora packages.

Then publish the distributions to PyPI, from the `master` branch (build them again from
the tagged commit if needed):

```sh
git switch master
git pull
make clean build
uv publish --index testpypi     # optional: check the result on https://test.pypi.org/
uv publish                      # requires a PyPI API token (UV_PUBLISH_TOKEN)
```

Finally, merge `master` back into `develop`, so that `develop` contains the release:

```sh
git switch develop
git pull
git merge --no-ff master
git push
```

## After the release

- Check the [PyPI page](https://pypi.org/project/Deprecated/) and the
  [documentation](https://deprecated.readthedocs.io/en/latest/) of the new version.
- Close the GitHub milestone of the release, if any.
