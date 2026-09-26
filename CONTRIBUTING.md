# How to contribute to Deprecated Library

Thank you for considering contributing to Deprecated!

## Support questions

Please, don't use the issue tracker for this. Use one of the following
resources for questions about your own code:

- Ask on [Stack Overflow]. Search with Google first using:
  `site:stackoverflow.com deprecated decorator {search term, exception message, etc.}`

## Reporting issues

- Describe what you expected to happen.
- If possible, include a [minimal, complete, and verifiable example] to help
  us identify the issue. This also helps check that the issue is not with your
  own code.
- Describe what actually happened. Include the full traceback if there was an
  exception.
- List your Python, Deprecated and wrapt versions. If possible, check if this
  issue is already fixed in the repository.

## Submitting patches

- Include tests if your patch is supposed to solve a bug, and explain
  clearly under which circumstances the bug happens. Make sure the test fails
  without your patch.
- Follow [PEP8]: the code is linted and formatted with Ruff (line length: 100).

### First time setup

- Download and install the [latest version of git].

- Configure git with your [username] and [email]:

  ```
  git config --global user.name 'your name'
  git config --global user.email 'your email'
  ```

- Make sure you have a [GitHub account].

- Fork Deprecated to your GitHub account by clicking the [Fork] button.

- [Clone] your GitHub fork locally:

  ```
  git clone https://github.com/{username}/deprecated.git
  cd deprecated
  ```

- Add the main repository as a remote to update later:

  ```
  git remote add upstream https://github.com/laurent-laporte-pro/deprecated.git
  git fetch upstream
  ```

- Install [uv] and [Hatch] (Python 3.12 or newer is required):

  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  uv tool install hatch
  ```

- Create the virtual environment and install Deprecated in editable mode
  with the development dependencies (locked in `uv.lock`):

  ```
  uv sync
  ```

### Start coding

- Create a branch to identify the issue you would like to work on (e.g.
  `2287-dry-test-suite`)
- Using your favorite editor, make your changes, [committing as you go].
- Follow [PEP8]: the code is linted and formatted with Ruff (line length: 100).
- Include tests that cover any code changes you make. Make sure the test fails
  without your patch. See [Running the tests](#running-the-tests).
- Push your commits to GitHub and [create a pull request].
- Celebrate 🎉

### Running the tests

Run the basic test suite with:

```
uv run pytest
```

This only runs the tests for the current environment. Whether this is relevant
depends on which part of Deprecated you're working on. GitHub Actions will run the full
suite when you submit your pull request.

The full test suite tests multiple combinations of Python (3.12 and newer)
and wrapt versions. Hatch downloads the missing Python interpreters with uv. Run:

```
hatch test --all
```

### Running the quality checks

The following checks are run by the CI and must pass before merging:

```
hatch check code    # lint with Ruff
hatch check fmt     # verify the formatting with Ruff (use --fix to reformat)
hatch check types   # type-check with mypy (strict mode)
```

### Running test coverage

Generating a report of lines that do not have test coverage can indicate
where to start contributing. Run `pytest` using `coverage` and generate a
report on the terminal and as an interactive HTML document:

```
uv run pytest --cov --cov-report term-missing --cov-report html
# then open htmlcov/index.html
```

Read more about [coverage](https://coverage.readthedocs.io).

### `make` targets

Deprecated provides a `Makefile` with various shortcuts, based on uv and Hatch
(run `make help` to list them):

- `make install` creates the virtual environment with the locked dependencies
- `make test` runs the basic test suite with `pytest`
- `make cov` runs the basic test suite with `coverage`
- `make test-all` runs the full test suite with `hatch test --all`
- `make check` verifies the lockfile and runs the quality checks with `hatch check`
- `make fix` fixes the lint errors and reformats the code
- `make docs` builds the HTML documentation
- `make docs-live` serves the HTML documentation, rebuilt and reloaded on each change
- `make build` builds the source distribution and the wheel
- `make version` shows the current version, and `make bump-major`, `make bump-minor`,
  `make bump-patch` bump it with `hatch version` (see the [release process](docs/source/release.md))
- `make clean` removes the build artifacts and the caches

### Generating the documentation

The documentation is automatically generated with ReadTheDocs for each git push on master.
You can also generate it manually using Sphinx.

To generate the HTML documentation, run:

```
uv run --group docs sphinx-build -b html -d dist/docs/doctrees docs/source/ dist/docs/html/
```

To preview the documentation while editing it, run `make docs-live` and open
<http://127.0.0.1:8000>: the pages are rebuilt and the browser is reloaded on each change
of the documentation or of the docstrings (`src/deprecated/`).

[clone]: https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork
[committing as you go]: http://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes
[create a pull request]: https://help.github.com/articles/creating-a-pull-request/
[email]: https://help.github.com/articles/setting-your-commit-email-address-in-git/
[fork]: https://github.com/laurent-laporte-pro/deprecated/fork
[github account]: https://github.com/join
[hatch]: https://hatch.pypa.io/latest/
[latest version of git]: https://git-scm.com/downloads
[minimal, complete, and verifiable example]: https://stackoverflow.com/help/mcve
[pep8]: https://pep8.org/
[stack overflow]: https://stackoverflow.com/search?q=python+deprecated+decorator
[username]: https://help.github.com/articles/setting-your-username-in-git/
[uv]: https://docs.astral.sh/uv/
