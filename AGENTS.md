# AGENTS.md

Guidance for AI coding agents working in this repository.

**Deprecated** is a small, published open-source library (`pip install Deprecated`) that
provides the `@deprecated` decorator for classes, functions and methods. It is a
Python 3.12+ project managed with **uv** (environment, lockfile) and **Hatch** (version,
quality checks, test matrix). Its only runtime dependency is `wrapt >= 1.16, < 3`.

Everything in `src/deprecated/` is **public API used by many downstream projects**: keep
changes backward compatible unless a major release is explicitly being prepared.

## Commands

```sh
uv sync                     # create .venv with the locked dev dependencies (make install)
uv run pytest               # test suite, current Python (make test)
uv run pytest tests/test_deprecated.py::test_classic_deprecated_function__warns   # a single test
uv run pytest -k sphinx     # tests matching a keyword
make cov                    # tests with coverage (terminal + htmlcov/)
make test-all               # hatch test --all: every Python x wrapt combination
WRAPT_DISABLE_EXTENSIONS=1 uv run pytest   # tests with the pure Python wrapt (run in CI)

make check                  # uv lock --check + hatch check code / fmt / types (what CI runs)
make fix                    # ruff --fix and ruff format
make docs-check             # Sphinx build, warnings are errors (what CI runs)
make docs-live              # docs preview with auto-rebuild (sphinx-autobuild)
make build                  # sdist + wheel
```

`hatch check code|fmt|types` run Ruff and mypy with the versions pinned in `pyproject.toml`
(identical to the `dev` group of `uv.lock`); `uv run ruff check .` and `uv run mypy` give the
same results from the project venv. Never edit `uv.lock` by hand: use `uv lock` / `uv add`.

## Architecture

Six modules in `src/deprecated/` (src layout, `py.typed` shipped):

- `classic.py` — `ClassicAdapter` (a `wrapt.AdapterFactory`) and the `deprecated()` decorator.
  `deprecated` accepts three call forms (`@deprecated`, `@deprecated("reason")`,
  `@deprecated(reason=..., version=..., action=..., category=..., extra_stacklevel=...)`),
  typed with `@overload`. The adapter behaves differently by target:
  - **routines** are wrapped with `wrapt.decorator` (transparent proxy, keeps the signature);
  - **classes** are *not* wrapped: their `__new__` is patched in place to emit the warning.
  - `warn()` uses `warnings.warn(..., skip_file_prefixes=SKIP_FILE_PREFIXES)` so the warning
    location always points at user code, whatever the wrapt implementation (C extension or
    pure Python) and the nesting depth. Anything touching stack levels must keep that invariant
    (tests check the reported file/line).
- `sphinx.py` — `SphinxAdapter(ClassicAdapter)` plus `versionadded`, `versionchanged` and
  `deprecated`. It rewrites the docstring by appending a `.. directive:: version` block (text
  wrapped at `line_length`); only `deprecated` also emits a warning (via the parent adapter),
  and `get_deprecated_msg` strips Sphinx roles (`:func:` ...) from the message.
- `google.py` / `numpy.py` — `GoogleAdapter` / `NumpyAdapter(ClassicAdapter)` plus
  `versionadded`, `versionchanged` and `deprecated`, built like `sphinx.py`: they add (or
  extend) a `Version added` / `Version changed` / `Deprecated` section to Google-style
  (`Header:`) or NumPy-style (hyphen-underlined header) docstrings.
- `params.py` — `deprecated_params` (alias of the `DeprecatedParams` class) warns when
  deprecated *parameters* are passed. Stacked `@deprecated_params` decorators are merged
  through the `__deprecated_params__` attribute (`_DecoratorStack`) so each parameter warns
  once. It uses `functools.wraps`, not wrapt.
- `__init__.py` — exports `deprecated` and `deprecated_params`, and holds `__version__`,
  the **single source of the version** (read by Hatch, updated with `hatch version`).

Tests live in `tests/` (`test*.py`, pytest); `tests/deprecated_params/` holds the demo
scenarios of `deprecated_params`. Documentation is Sphinx + MyST Markdown in `docs/source/`;
the scripts in `docs/source/` (`tutorial/`, `sphinx/`, `google/`, `numpydoc/`) are executed
examples whose output (including warning line numbers) is quoted in the pages, which is why Ruff does not reformat `*.md`.

## Python conventions

Enforced by `pyproject.toml` (Ruff + mypy strict); CI fails on any violation.

- Python **3.12+** syntax: PEP 695 generics (`def f[T: Deprecatable](...)`, `type X = ...`),
  built-in generics, `X | None` unions, `collections.abc` types for parameters.
- **Never** `from __future__ import annotations` (banned by a Ruff `TID` rule).
- Every function in `src/` is fully annotated (`ANN` rules, mypy `strict`,
  `warn_unreachable`). `*args: Any, **kwargs: Any` is accepted for pass-through wrappers.
  Every `# type: ignore` / `# noqa` must carry its error code and ideally a reason.
  Test code is exempt from annotation rules.
- Ruff: line length **100**, double quotes, **one import per line** (`force-single-line`),
  no `print()` outside tests and docs.
- Naming: `snake_case` functions/modules, `PascalCase` classes, `SCREAMING_SNAKE_CASE`
  module constants; private helpers prefixed with `_`.
- Errors: raise a precise built-in exception (`TypeError`, `ValueError`...), never bare
  `Exception`. The library emits `warnings` (default category `DeprecationWarning`); it does
  not log.
- Docstrings are reStructuredText (Sphinx autodoc): document `:param:` / `:return:`, and add
  `.. versionadded::`, `.. versionchanged::` or `.. deprecated::` with the upcoming version
  to any public behaviour you change.
- Bug fixes come with a test that fails without the fix; behaviour must hold on every
  supported Python (3.12–3.14) and wrapt version (1.16, 1.17, 2.x) of the Hatch matrix.

## Git workflow

- Branches: `develop` is the integration branch and receives the pull requests; `master`
  holds the releases. Work on short-lived branches created from `develop`:
  `feature/<slug>`, `fix/<slug>` (optionally prefixed by the GitHub issue number, e.g.
  `fix/123-nested-class-stacklevel`). `release/X.Y.Z` and `hotfix/X.Y.Z` branches target
  `master` (see `docs/source/release.md`).
- Commits follow **Conventional Commits**: `<type>(<scope>): <description>`, imperative,
  lowercase, e.g. `fix: emit one warning per parameter with stacked @deprecated_params`,
  `build(docs): use Sphinx 9.1`. Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`,
  `build`, `ci`, `perf`, `revert`.
- Pull requests target `develop`, follow `.github/PULL_REQUEST_TEMPLATE.md` (what the patch
  does, linked issues), and add a `CHANGELOG.md` entry for code changes. The CI
  (`.github/workflows/python-package.yml`: quality checks, tests on Linux/macOS/Windows,
  wrapt matrix, docs) must be green before merging.
- Never force-push `develop` or `master`; never rewrite someone else's branch.
- Releases: bump with `hatch version <major|minor|patch>` (never edit the version elsewhere
  except `python-deprecated.spec` and the logo (`docs/source/_static/logo.svg`), as listed in the release guide).
  Tags use the **`vX.Y.Z`** form and are created by GitHub when the release is published,
  not locally.

## Changelog

`CHANGELOG.md` (3.x; older series in `CHANGELOG-1.*.md`) follows Keep a Changelog. Add
entries under the topmost `## vX.Y.Z (unreleased)` section, in the right category (`Added`,
`Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`, `Documentation`, `Other`), written
for library users in plain GitHub Markdown (no MyST roles; `> [!WARNING]` for breaking
changes).
