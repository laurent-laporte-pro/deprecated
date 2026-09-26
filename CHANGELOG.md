# Changelog 3.x

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v3.0.0 (unreleased)

Major release: Python 3.12+ modernization

> [!WARNING]
> This release drops the support of Python 2.7 and of Python 3 versions older than 3.12.
> Use Deprecated 1.3.x on these versions.

> [!NOTE]
> There is no 2.x release: the major version 3 was chosen to match Python 3.

### Changed

- Require Python >= 3.12 and wrapt >= 1.16 (first wrapt release supporting Python 3.12).
- Remove the `inspect2` dependency (it was only used on Python 2).
- Remove the Python 2 compatibility constructs (`u""` literals, `coding` cookies,
  `class Foo(object)`, `super(Class, self)`, `OrderedDict`...).
- Remove the undocumented `deprecated.classic.string_types` compatibility tuple.
  A `bytes` positional *reason* is still accepted by `@deprecated`, as before.
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
- Remove the `deprecated.__date__` attribute (the release dates are in the changelog).
- Update the Fedora RPM spec file to the `%pyproject_*` macros.

### Added

- Add the `deprecated.google` module: the `@deprecated`, `@versionadded` and `@versionchanged`
  decorators insert a `Deprecated:`, `Version added:` or `Version changed:` section
  in [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
  docstrings (see the "Google decorators" page of the documentation).
- Add the `deprecated.numpy` module: the `@deprecated`, `@versionadded` and `@versionchanged`
  decorators insert a `Deprecated`, `Version added` or `Version changed` section
  in [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html)
  docstrings (see the "NumPy decorators" page of the documentation).
- Add the `ClassicAdapter.warn()` method used to emit the deprecation warning
  (can be overridden by custom adapters).
- Add Python 3.12 type annotations to the public API and ship the `py.typed` marker (PEP 561):
  the decorators preserve the signature of the decorated functions and classes.
- Add the `hatch check code` (Ruff lint), `hatch check fmt` (Ruff format)
  and `hatch check types` (mypy, strict mode) quality checks.
- Document the release process (`docs/source/release.md`).
- Add non-regression tests for the behaviours which differ between Python 2 and Python 3.
- Add `__all__` to the `deprecated` package: `from deprecated import *` only exports
  `deprecated` and `deprecated_params`.

### Fixed

- Deprecated functions and methods can now be pickled (by reference, like regular functions),
  so they can be used with `multiprocessing` and the *spawn* start method (the default one on
  Windows and macOS), for instance as a `Process` target or with `Pool.map()`.
  Previously, pickling failed with `NotImplementedError: object proxy must define __reduce_ex__()`
  ([#16](https://github.com/laurent-laporte-pro/deprecated/issues/16)).
- When a deprecated class inherits from a deprecated class, all the deprecation warnings now refer
  to the user code (previously, the warning of the parent class referred to `classic.py`).
  The warnings are emitted with `skip_file_prefixes` (Python 3.12+): the frames of this library
  and of wrapt are skipped, whatever the wrapt implementation (C extension or pure Python).
- Stacked `@deprecated_params` decorators now emit only one warning for each deprecated
  parameter: the message (and category) of the outermost decorator wins, as documented
  in the tutorial. The warnings refer to the caller.
- The `test_sphinx_metaclass` tests now test the Sphinx decorator (they tested the classic one).

### Documentation

- Convert the documentation from reStructuredText to Markdown (MyST), built with Sphinx 9.1
  and MyST-Parser 5.1. The API page remains in reStructuredText (autodoc), and the docstrings
  are still written in reStructuredText.
- Convert the root files to plain Markdown, readable on GitHub: `CHANGELOG.md`,
  `CONTRIBUTING.md` and `LICENSE.md`.
- Declare the documentation dependencies in the `docs` dependency group of `pyproject.toml`
  (`docs/requirements.txt` is removed); ReadTheDocs installs them with uv.
- Check the documentation build in the CI (`make docs-check`: warnings are errors).
- Rewrite the white paper: state of the art of deprecation in Python (warning categories and
  stack level, PEP 702 and the type checkers, the CPython policy, practices of major Open Source
  projects, best practices), and how to combine `warnings.deprecated` with this library.
- Remove the ebook, LaTeX, manual page and Texinfo configuration of the documentation (HTML only),
  with the files used by the ebook (cover, title page and blurb).
- Rework the README: a short presentation, the warning emitted, the options of `@deprecated`,
  `@deprecated_params`, and how the library complements `warnings.deprecated` (PEP 702).
  The "Authors" section now tells who started the library and who maintains it.
- New logo (a "best before: next major" price tag), shown in the README and on the home page
  of the documentation; it replaces the rusty tools image.

### Other

- Run the CI with uv and Hatch on Python 3.12, 3.13 and 3.14 (Linux, macOS and Windows),
  plus the wrapt compatibility matrix and the pure Python implementation of wrapt.
