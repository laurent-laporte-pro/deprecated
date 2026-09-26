# Deprecated Decorator

![Deprecated: a price tag reading "@deprecated, best before: next major"](https://raw.githubusercontent.com/laurent-laporte-pro/deprecated/master/docs/source/_static/logo.svg)

Python `@deprecated` decorator to deprecate old python classes, functions or methods.

[![license](https://img.shields.io/badge/license-MIT-blue?logo=opensourceinitiative&logoColor=white)](https://raw.githubusercontent.com/laurent-laporte-pro/deprecated/master/LICENSE.md)
[![GitHub release](https://img.shields.io/github/v/release/laurent-laporte-pro/deprecated?logo=github&logoColor=white)](https://github.com/laurent-laporte-pro/deprecated/releases/latest)
[![PyPI](https://img.shields.io/pypi/v/deprecated?logo=pypi&logoColor=white)](https://pypi.org/project/Deprecated/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/laurent-laporte-pro/deprecated/python-package.yml?logo=github&logoColor=white)](https://github.com/laurent-laporte-pro/deprecated/actions/workflows/python-package.yml)
[![Coveralls branch](https://img.shields.io/coverallsCoverage/github/laurent-laporte-pro/deprecated?logo=coveralls&logoColor=white)](https://coveralls.io/github/laurent-laporte-pro/deprecated?branch=master)
[![Read the Docs (version)](https://img.shields.io/readthedocs/deprecated/latest?logo=readthedocs&logoColor=white)](https://deprecated.readthedocs.io/en/latest/?badge=latest)

Removing a function from a library breaks the code of its users. Deprecating it first gives
them time to migrate: the Deprecated library marks classes, functions, methods and parameters
as deprecated, emits a warning that points at the calling code, and can document the deprecation
in the docstring.

## Installation

```shell
pip install Deprecated
```

Deprecated requires Python 3.12+ and [wrapt](https://pypi.org/project/wrapt/).

## Usage

Decorate a deprecated function, method or class with `@deprecated`:

```python
from deprecated import deprecated


@deprecated(reason="use new_function", version="2.1.0")
def some_old_function(x, y):
    return x + y


some_old_function(1, 2)
```

Each call emits a warning located at the calling line:

```text
example.py:9: DeprecationWarning: Call to deprecated function (or staticmethod) some_old_function. (use new_function) -- Deprecated since version 2.1.0.
```

`@deprecated` can also be used without arguments, and accepts other options:
`category` (e.g. `FutureWarning` instead of `DeprecationWarning`), `action` (a local warning
filter, e.g. `"error"`) and `extra_stacklevel` (for wrappers of deprecated functions).

To deprecate a *parameter* rather than the whole function, use `@deprecated_params`:

```python
from deprecated import deprecated_params


@deprecated_params("color", reason="'color' is ignored, use 'style'")
def draw(shape, color=None, style=None):
    ...
```

Calling `draw("circle", color="red")` emits `DeprecationWarning: 'color' is ignored, use 'style'`.

## Documenting the life cycle

The Deprecated library can also document the life cycle of your functions and classes:
the `@deprecated`, `@versionadded` and `@versionchanged` decorators update the docstring,
according to your docstring format:

- `deprecated.sphinx`: reStructuredText directives (`.. deprecated:: 1.2.0`),
- `deprecated.google`: Google style sections (`Deprecated:`),
- `deprecated.numpy`: NumPy style sections (`Deprecated` underlined with hyphens).

```python
from deprecated.google import deprecated
from deprecated.google import versionadded


@deprecated(reason="use another function", version="1.2.0")
@versionadded(version="1.0.0")
def some_old_function(x, y):
    """Add two numbers.

    Args:
        x: first number.
        y: second number.
    """
    return x + y
```

The docstring of `some_old_function` ends with:

```text
Version added:
    1.0.0

Deprecated:
    1.2.0: use another function
```

## Why not `warnings.deprecated`?

Since Python 3.13, [`warnings.deprecated`](https://docs.python.org/3/library/warnings.html#warnings.deprecated)
([PEP 702](https://peps.python.org/pep-0702/)) emits a runtime warning and lets the type
checkers report the use of deprecated objects. Deprecated complements it with version numbers,
docstring updates (Sphinx, Google, NumPy), local warning filters and deprecated parameters.
Both can be combined, see the [white paper](https://deprecated.readthedocs.io/en/latest/white_paper.html).

See the [documentation](https://deprecated.readthedocs.io/en/latest/) for more details.

## Authors

Deprecated was started by [Marcos CARDOSO](https://github.com/vrcmarcos), building on the
recipes shared in [this Stack Overflow discussion](https://stackoverflow.com/questions/2536307)
by [Leandro REGUEIRO](https://stackoverflow.com/users/1336250/leandro-regueiro),
[Patrizio BERTONI](https://stackoverflow.com/users/1315480/patrizio-bertoni) and
[Eric WIESER](https://stackoverflow.com/users/102441/eric).

[Laurent LAPORTE](https://github.com/laurent-laporte-pro) has been the main author and
maintainer of the library for many years.
