# Changelog 3.x

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v3.0.0 (2026-09-26)

Major release: Python 3.12+ modernization

> [!WARNING]
> This release drops the support of Python 2.7 and of Python 3 versions older than 3.12.
> Use Deprecated 1.3.x on these versions: pip keeps resolving to 1.3.x on Python < 3.12.

> [!IMPORTANT]
> **Upgrading from 1.x** — the public API (`@deprecated`, `@deprecated_params`,
> `deprecated.sphinx`, `ClassicAdapter`) is unchanged, but check the following points:
>
> - wrapt >= 1.16 is required (was >= 1.10);
> - `deprecated.__date__` and `deprecated.classic.string_types` are removed;
> - `from deprecated import *` only exports `deprecated` and `deprecated_params`;
> - stacked `@deprecated_params` decorators emit one warning per deprecated parameter;
> - the warnings of deprecated subclasses now refer to the user code: tests which assert
>   the file name or the line number of a warning may need to be updated.

> [!NOTE]
> There is no 2.x release: the major version 3 was chosen to match Python 3.

### Changed

- Require Python >= 3.12 and wrapt >= 1.16 (first wrapt release supporting Python 3.12).
  See PR #102.
- Migrate the packaging from setuptools (`setup.py`/`setup.cfg`/`MANIFEST.in`) to
  `pyproject.toml` with the Hatchling build backend; the version is read from
  `src/deprecated/__init__.py`.
- Adopt the `src` layout: the package moves to `src/deprecated`
  (the tests stay in `tests` and the documentation in `docs`).
- Manage the project with uv (`uv.lock`) and Hatch: tox is dropped and replaced
  by the `hatch test` matrix.
- Modernize the `Makefile` (uv/Hatch based targets, run `make help`).
- Replace bump2version by `hatch version <major|minor|patch>`: the version is only defined
  in `src/deprecated/__init__.py`, and the git tag is created by GitHub when the release
  is published.
- Update the Fedora RPM spec file to the `%pyproject_*` macros.

### Removed

- Remove the `inspect2` dependency (it was only used on Python 2). See PR #102.
- Remove the Python 2 compatibility constructs (`u""` literals, `coding` cookies,
  `class Foo(object)`, `super(Class, self)`, `OrderedDict`...). See PR #102.
- Remove the undocumented `deprecated.classic.string_types` compatibility tuple.
  A `bytes` positional *reason* is still accepted by `@deprecated`, as before. See PR #102.
- Remove the `deprecated.__date__` attribute (the release dates are in the changelog).
  See PR #102.

### Added

- Add the `deprecated.google` module: the `@deprecated`, `@versionadded` and `@versionchanged`
  decorators insert a `Deprecated:`, `Version added:` or `Version changed:` section
  in [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
  docstrings (see the ["Google" decorators](https://deprecated.readthedocs.io/en/latest/google_deco.html)
  page). See PR #105.
- Add the `deprecated.numpy` module: the `@deprecated`, `@versionadded` and `@versionchanged`
  decorators insert a `Deprecated`, `Version added` or `Version changed` section
  in [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html)
  docstrings (see the ["NumPy" decorators](https://deprecated.readthedocs.io/en/latest/numpy_deco.html)
  page). See PR #106.
- Add the `ClassicAdapter.warn()` method used to emit the deprecation warning
  (can be overridden by custom adapters). See PR #102.
- Add Python 3.12 type annotations to the public API and ship the `py.typed` marker (PEP 561):
  the decorators preserve the signature of the decorated functions and classes. See PR #102.
- Add `__all__` to the `deprecated` package: `from deprecated import *` only exports
  `deprecated` and `deprecated_params`. See PR #102.

### Fixed

- Deprecated functions and methods can now be pickled (by reference, like regular functions),
  so they can be used with `multiprocessing` and the *spawn* start method (the default one on
  Windows and macOS), for instance as a `Process` target or with `Pool.map()`.
  Previously, pickling failed with `NotImplementedError: object proxy must define __reduce_ex__()`
  ([#16](https://github.com/laurent-laporte-pro/deprecated/issues/16)). See PR #108 and PR #111
  (a function decorated with `@deprecated` above `@staticmethod` could not be pickled).
- When a deprecated class inherits from a deprecated class, all the deprecation warnings now refer
  to the user code (previously, the warning of the parent class referred to `classic.py`).
  The warnings are emitted with `skip_file_prefixes` (Python 3.12+): the frames of this library
  and of wrapt are skipped, whatever the wrapt implementation (C extension or pure Python).
  See PR #102.
- Stacked `@deprecated_params` decorators now emit only one warning for each deprecated
  parameter: the message (and category) of the outermost decorator wins, as documented
  in the tutorial. The warnings refer to the caller. See PR #102.

### Documentation

- Convert the documentation from reStructuredText to Markdown (MyST), built with Sphinx 9.1
  and MyST-Parser 5.1. The API page remains in reStructuredText (autodoc), and the docstrings
  are still written in reStructuredText. See PR #103.
- Convert the root files to plain Markdown, readable on GitHub: `CHANGELOG.md`,
  `CONTRIBUTING.md` and `LICENSE.md`.
- Declare the documentation dependencies in the `docs` dependency group of `pyproject.toml`
  (`docs/requirements.txt` is removed); ReadTheDocs installs them with uv.
- Check the documentation build in the CI (`make docs-check`: warnings are errors).
- Rewrite the white paper: state of the art of deprecation in Python (warning categories and
  stack level, PEP 702 and the type checkers, the CPython policy, practices of major Open Source
  projects, best practices), and how to combine `warnings.deprecated` with this library.
  See PR #104.
- Remove the ebook, LaTeX, manual page and Texinfo configuration of the documentation (HTML only),
  with the files used by the ebook (cover, title page and blurb).
- Rework the README: a short presentation, the warning emitted, the options of `@deprecated`,
  `@deprecated_params`, and how the library complements `warnings.deprecated` (PEP 702).
  The "Authors" section now tells who started the library and who maintains it.
- New logo (a "best before: next major" price tag), shown in the README and on the home page
  of the documentation; it replaces the rusty tools image. See PR #109.
- Switch the documentation to the [Furo](https://pradyunsg.me/furo/) theme, with light, dark
  and automatic (system preference) modes, and the red of the logo as accent color.
  The code is highlighted with the Lovelace (light) and Gruvbox dark (dark) Pygments styles,
  tuned for contrast (WCAG AA). See PR #110.
- Add `make docs-live` to preview the documentation while editing it: the pages are rebuilt
  and the browser is reloaded on each change (sphinx-autobuild, `docs-live` dependency group).
  See PR #110.
- Present the Google and NumPy docstring decorators in the documentation. See PR #107.
- Document the release process (`docs/source/release.md`).
- Fix the outputs quoted in the tutorial and in the Sphinx page, stale references and typos
  of the documentation and of the docstrings. See PR #111.

### Other

- Run the CI with uv and Hatch on Python 3.12, 3.13 and 3.14 (Linux, macOS and Windows),
  plus the wrapt compatibility matrix (wrapt 1.16, 1.17 and 2.x on every supported Python)
  and the pure Python implementation of wrapt. See PR #102 and PR #111.
- Add the `hatch check code` (Ruff lint), `hatch check fmt` (Ruff format)
  and `hatch check types` (mypy, strict mode) quality checks. See PR #102.
- Add non-regression tests for the behaviours which differ between Python 2 and Python 3,
  and make the `test_sphinx_metaclass` tests test the Sphinx decorator. See PR #102.
- Bump the GitHub Actions versions. See PR #99.
- Run CodeQL on the `develop` and `master` branches, and add Dependabot version updates
  (GitHub Actions and `uv.lock`). See PR #111.
- Publish the coverage to Coveralls (README badge), and fail the tests below 95% of coverage.
  See PR #111.
- Add `AGENTS.md` and `CLAUDE.md`: guidance for AI coding agents.
