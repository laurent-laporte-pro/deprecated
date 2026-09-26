(installation)=

# Installation

## Python Version

Our project supports Python 3.12 and newer versions.
We recommend using the latest version of Python 3 whenever possible.

:::{versionchanged} 3.0.0
Support for Python 2.7 and Python 3 versions older than 3.12 has been dropped.
Use Deprecated 1.3.x on these versions.
:::

## Dependencies

This library uses the [Wrapt] library as a basis to construct
function wrappers and decorator functions.

The table below shows the compatibility matrix between Python versions and the `wrapt` versions that have been
tested to date. Recent versions are listed first.

```{list-table} Compatibility matrix (tested versions)
:header-rows: 1
:widths: 25 9 9 9

* - Python / wrapt
  - 2.x
  - 1.17
  - 1.16
* - py3.14
  - ✓
  - ✓
  - ✗
* - py3.13
  - ✓
  - ✓
  - ✗
* - py3.12
  - ✓
  - ✓
  - ✓
```

Legend: ✓ = tested and compatible ; ✗ = incompatible, ? = untested but expected to work

### Development dependencies

The project is managed with [uv]: the development dependencies are declared in the `dev`
dependency group of the {file}`pyproject.toml` file, and locked in the {file}`uv.lock` file.
They are installed with `uv sync`.

- [pytest] is a framework which makes it easy to write small tests,
  yet scales to support complex functional testing for applications and libraries…
- [pytest-cov] is a [pytest] plugin used to produce coverage reports.
- [Ruff] is used to lint and format the source code.
- [mypy] is used to type-check the source code.

The quality checks and the test matrix are run with [Hatch] (installed with `uv tool install hatch`):

- `hatch check code` lints the code with Ruff,
- `hatch check fmt` verifies the formatting with Ruff,
- `hatch check types` type-checks the code with mypy,
- `hatch test --all` runs the test suite on all supported Python and wrapt versions.

The version is defined in {file}`src/deprecated/__init__.py` and updated with `hatch version`
(see {ref}`release`), and [sphinx] (with the [MyST] Markdown parser) is used to build
the documentation: its dependencies are declared in the `docs` dependency group
(`uv sync --group docs`, or `make docs`).

## Virtual environments

Use a virtual environment to manage the dependencies for your project, both in
development and in production.

What problem does a virtual environment solve? The more Python projects you
have, the more likely it is that you need to work with different versions of
Python libraries, or even Python itself. Newer versions of libraries for one
project can break compatibility in another project.

Virtual environments are independent groups of Python libraries, one for each
project. Packages installed for one project will not affect other projects or
the operating system's packages.

Python 3 comes bundled with the {mod}`venv` module to create virtual
environments.

(install-create-env)=

### Create an environment

Create a project folder and a {file}`venv` folder within:

```sh
mkdir myproject
cd myproject
python3 -m venv venv
```

On Windows:

```bat
py -3 -m venv venv
```

### Activate the environment

Before you work on your project, activate the corresponding environment:

```sh
. venv/bin/activate
```

On Windows:

```bat
venv\Scripts\activate
```

Your shell prompt will change to show the name of the activated environment.

## Install Deprecated

Within the activated environment, use the following command to install Deprecated:

```sh
pip install Deprecated
```

### Living on the edge

If you want to work with the latest Deprecated code before it's released, install or
update the code from the develop branch:

```sh
pip install -U https://github.com/laurent-laporte-pro/deprecated/archive/develop.tar.gz
```

[hatch]: https://hatch.pypa.io/latest/
[mypy]: https://mypy.readthedocs.io/en/stable/
[pytest]: https://docs.pytest.org/en/latest/
[pytest-cov]: http://pytest-cov.readthedocs.io/en/latest/
[ruff]: https://docs.astral.sh/ruff/
[sphinx]: http://www.sphinx-doc.org/en/stable/index.html
[uv]: https://docs.astral.sh/uv/
[wrapt]: http://wrapt.readthedocs.io/en/latest/
[myst]: https://myst-parser.readthedocs.io/
