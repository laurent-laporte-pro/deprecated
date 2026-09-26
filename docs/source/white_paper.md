(white_paper)=

# White Paper

This white paper describes the state of the art of deprecation in Python (2026):
the building blocks provided by the language, the deprecation marker of the type system
(PEP 702), the policies of the Python Standard Library and of major Open Source projects,
and the resulting best practices. It ends with the place of the Deprecated Library
in this landscape.

## What is a good deprecation?

A deprecation announces that a feature (a function, a class, a method, a parameter,
a module attribute…) will be removed or changed in a backward incompatible way.
It gives the users of a library the time to migrate their code.

A good deprecation answers four questions:

- **What** is deprecated?
- **Since when** (in which version)?
- **What should be used instead?**
- **When** will it be removed?

And it reaches the users through several channels:

1. a **runtime warning**, emitted when the deprecated feature is used;
2. a **static diagnostic**, reported by type checkers and IDEs before the code even runs;
3. the **documentation** (docstring, API reference, changelog, migration guide);
4. a **schedule**, which is eventually honored: the feature is really removed.

## The building blocks of the language

### Warning categories: who sees what?

Python emits deprecation warnings with {func}`warnings.warn`.
The warning category determines who sees the warning with the default warning filters
([PEP 565], Python 3.7+):

```{list-table}
:header-rows: 1
:widths: 30 30 40

* - Category
  - Shown by default?
  - Audience
* - {exc}`DeprecationWarning`
  - Only when triggered by code in `__main__`, and by test runners like pytest
  - Developers using the API (libraries, applications under development)
* - {exc}`PendingDeprecationWarning`
  - No
  - Early notice for developers: the feature will be deprecated later
* - {exc}`FutureWarning`
  - Yes
  - End users of applications: the behavior will change
```

Custom subclasses are common to allow a precise filtering, for instance:
`RemovedInDjango70Warning` (Django), `Pandas4Warning` (pandas),
`MatplotlibDeprecationWarning` (Matplotlib) or `SADeprecationWarning` (SQLAlchemy).

### The stack level

A deprecation warning must point to the **caller** of the deprecated feature, not to the library
itself: this is the role of the *stacklevel* argument of {func}`warnings.warn`.
Getting it right is harder than it seems (decorators, wrappers, inheritance…):
pandas even computes it dynamically with an internal `find_stack_level()` helper.

Since Python 3.12, the *skip_file_prefixes* argument makes this robust: the frames of the given
files are skipped, so the warning always refers to the first frame outside of the library:

```python
import os
import warnings

_LIB_DIR = os.path.dirname(__file__) + os.sep


def old_function():
    warnings.warn(
        "old_function() is deprecated since 2.0 and will be removed in 3.0, "
        "use new_function() instead",
        DeprecationWarning,
        stacklevel=2,
        skip_file_prefixes=(_LIB_DIR,),
    )
```

### Deprecating a module attribute

A module attribute (a constant, an alias, a function moved elsewhere…) can be deprecated
with a module-level `__getattr__` ([PEP 562]), which is only called for the missing names:

```python
# mylib/__init__.py
import warnings

from mylib.core import new_function

_DEPRECATED_ALIASES = {"old_function": "new_function"}


def __getattr__(name: str) -> object:
    if new_name := _DEPRECATED_ALIASES.get(name):
        warnings.warn(
            f"{name} is deprecated, use {new_name} instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return globals()[new_name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
```

Since `__getattr__` is only called for missing names, the deprecated attribute must not be defined
in the module namespace: only its access through `__getattr__` emits the warning.

## Deprecation in the type system: PEP 702

[PEP 702] (Python 3.13) adds the {func}`warnings.deprecated` decorator, also available for older
Python versions in [typing_extensions](https://typing-extensions.readthedocs.io/):

```python
from warnings import deprecated  # or: from typing_extensions import deprecated


@deprecated("Use new_api() instead")
def old_api() -> int:
    return 1


@deprecated("Use NewClass instead", category=FutureWarning)
class OldClass:
    pass
```

This decorator has two effects:

- **At runtime**, it emits a warning when the decorated function is called or the class is
  instantiated (or subclassed). The *category* (default: {exc}`DeprecationWarning`) and the
  *stacklevel* can be customized; with `category=None`, no runtime warning is emitted.
  The message is stored in the `__deprecated__` attribute, for runtime introspection.
- **Statically**, type checkers report every use of the deprecated object:

  ```text
  $ mypy --enable-error-code deprecated example.py
  example.py:9: error: function example.old_api is deprecated: Use new_api() instead  [deprecated]
  ```

  - mypy reports deprecations with the `deprecated` error code, which is disabled by default;
    `--report-deprecated-as-note` turns them into notes, and `--deprecated-calls-exclude` hides
    them for given functions, classes or packages.
  - Pyright and Pylance support PEP 702 too (`reportDeprecated`); the IDEs display deprecated
    objects with a strikethrough.

The decorator can also be applied to **one overload** of an overloaded function: this is the
typing way to deprecate a *signature*, for instance a parameter or a type of argument:

```python
from typing import overload
from warnings import deprecated


@overload
def area(width: float, height: float) -> float: ...
@overload
@deprecated("Passing a (width, height) tuple is deprecated, pass two arguments instead")
def area(width: tuple[float, float]) -> float: ...
def area(width, height=None):
    if height is None:
        width, height = width
    return width * height
```

Here, the type checkers only report the calls matching the deprecated overload.
Note that the runtime implementation still has to emit the warning itself for the deprecated case,
since the overloads don't exist at runtime.

PEP 702 has limits: only the decorated classes, functions and overloads are known to the type
checkers. Module attributes, parameters of non-overloaded functions or behavior changes are still
only visible at runtime and in the documentation.

## The policy of the Python Standard Library

The backward compatibility policy of CPython is defined by [PEP 387]:

- a deprecation lasts **at least two years** (two releases), and it is preferred to wait
  **five years** before removal;
- the deprecations are listed in the documentation, with the Python version of the removal
  (see [Deprecations](https://docs.python.org/3/deprecations/index.html)): for instance,
  `datetime.datetime.utcnow()` is deprecated since Python 3.12, in favor of
  `datetime.datetime.now(datetime.UTC)`;
- a **soft deprecation** can be used for an API which should no longer be used to write new code,
  but which remains safe to use in existing code: it is documented and tested, but not developed
  any further, and its removal is not scheduled. For instance, the {mod}`optparse`
  and {mod}`getopt` modules are soft deprecated in favor of {mod}`argparse`.

Internally, CPython uses a `warnings._deprecated(name, remove=(3, 14))` helper: it formats the
message with the removal version, and it **raises an error** once the removal version is reached,
so that a forgotten deprecation breaks the build of the next release instead of lasting forever.
For instance, the AST node classes `ast.Num`, `ast.Str`… are deprecated since Python 3.8, emit a
warning with this helper since Python 3.12 (`remove=(3, 14)`), and were removed in Python 3.14.

## Practices of major Open Source projects

```{list-table}
:header-rows: 1
:widths: 18 82

* - Project
  - Practice
* - [NumPy]
  - NEP 23: deprecation warnings for at least two releases (one year) before removal. The message
    gives the version of the deprecation and of the removal. `VisibleDeprecationWarning` is used
    when end users must see the warning (likely a bug in the user code). NumPy 2.0 removed many
    deprecated aliases at once.
* - [pandas]
  - Three-stage policy (PDEP-17, pandas 3.0): a {exc}`DeprecationWarning` first, a {exc}`FutureWarning`
    in the last minor release before the next major one (for broader visibility), then removal in
    the major release. Dedicated classes like `pandas.errors.Pandas4Warning` name the version of
    the removal.
* - [Django]
  - A class per removal version (`RemovedInDjango70Warning`…), with the aliases
    `RemovedInNextVersionWarning` and `RemovedAfterNextVersionWarning`, so that projects can
    filter the warnings without updating their configuration at each release. A public
    [deprecation timeline](https://docs.djangoproject.com/en/dev/internals/deprecation/) lists the
    removals of each version.
* - [SQLAlchemy]
  - A migration mode for the 2.0 major release: in SQLAlchemy 1.4, the `RemovedIn20Warning`
    warnings are only emitted when the `SQLALCHEMY_WARN_20` environment variable is set. An application
    running its tests without these warnings (turned into errors) is ready for SQLAlchemy 2.0.
* - [Matplotlib]
  - A rich internal API (`matplotlib._api`): `deprecated(since, alternative=..., removal=...)`
    for functions, classes and properties, and dedicated decorators for signature changes:
    `rename_parameter`, `delete_parameter`, `make_keyword_only`.
* - [scikit-learn]
  - Renamed or removed public objects and parameters are still supported for two releases,
    with the `sklearn.utils.deprecated` decorator, which also updates the docstring.
* - [Pydantic]
  - Since Pydantic 2.7, `Field(deprecated=...)` accepts a message or a {func}`warnings.deprecated`
    instance: a warning is emitted when the field is accessed, and the generated JSON Schema
    contains `"deprecated": true`.
```

Common threads: a documented and scheduled policy, messages which give the versions and the
alternative, dedicated warning classes for filtering, and tools to deprecate *parameters*,
not only whole functions.

## Best practices

1. **Write a complete message**: what is deprecated, since which version, what to use instead,
   and when it will be removed.
2. **Choose the category for the audience**: {exc}`DeprecationWarning` for developers,
   {exc}`FutureWarning` for end users, {exc}`PendingDeprecationWarning` for an early notice.
   A dedicated subclass helps the users to filter the warnings of your library.
3. **Point to the caller**: check the *stacklevel* with tests, or use *skip_file_prefixes*.
4. **Make it visible to the type checkers** with {func}`warnings.deprecated`
   (or `typing_extensions.deprecated`), including on overloads to deprecate a signature.
5. **Document it**: `deprecated`, `versionchanged` and `versionadded` directives in the docstrings,
   an entry in the changelog, and a migration guide for large changes.
6. **Test it**: check that the warning is emitted (`pytest.deprecated_call()` or `pytest.warns()`),
   and run the test suite with the deprecation warnings turned into errors
   (`-W error::DeprecationWarning`, or the `filterwarnings` option of pytest), to detect the use
   of deprecated features of your own dependencies early.
7. **Schedule and honor the removal**: keep a deprecation timeline, and remove the deprecated
   features in the announced version. A test (or a helper like `warnings._deprecated`) can fail
   when the removal version is reached.
8. **Prefer a soft deprecation** for a stable API which is only discouraged: document it, but don't
   warn and don't schedule its removal.

## Where does the Deprecated Library fit?

The Deprecated Library predates PEP 702 and is complementary to {func}`warnings.deprecated`:

```{list-table}
:header-rows: 1
:widths: 40 30 30

* - Feature
  - {func}`warnings.deprecated`
  - Deprecated Library
* - Runtime warning for functions, methods and classes
  - Yes
  - Yes
* - Detection by type checkers and IDEs
  - Yes
  - No
* - Message built from a *reason* and a *version*
  - No (free message)
  - Yes
* - Docstring update (Sphinx directives, Google or NumPy sections)
  - No
  - Yes ({mod}`deprecated.sphinx`, {mod}`deprecated.google`, {mod}`deprecated.numpy`)
* - Local warning filter (*action*) and *extra_stacklevel*
  - No (only *stacklevel*)
  - Yes
* - Deprecation of parameters
  - Only through overloads (static only)
  - Yes, at runtime ({func}`~deprecated.params.deprecated_params`)
* - Python versions
  - 3.13+ (older versions: `typing_extensions`)
  - 3.12+
```

The type checkers only recognize {func}`warnings.deprecated` and `typing_extensions.deprecated`:
the `@deprecated` decorators of this library are not reported statically. To get the best of both
worlds, you can combine them: {func}`warnings.deprecated` with `category=None` for the static
detection only, and the Deprecated Library for the runtime warning and the documentation:

```python
import warnings

from deprecated.sphinx import deprecated


@warnings.deprecated("Use new_api() instead", category=None)  # type checkers and IDEs only
@deprecated(reason="Use :func:`new_api` instead", version="2.0")  # runtime warning + docstring
def old_api() -> int:
    """Old API."""
    return 1
```

With this combination, calling `old_api()` emits a single runtime warning (from the Deprecated
Library, pointing to the caller), the docstring contains the `.. deprecated:: 2.0` directive,
and the type checkers report every use of `old_api`.

## References

- [PEP 387] – Backwards Compatibility Policy
- [PEP 565] – Show DeprecationWarning in `__main__`
- [PEP 562] – Module `__getattr__` and `__dir__`
- [PEP 702] – Marking deprecations using the type system
- [warnings — Warning control](https://docs.python.org/3/library/warnings.html)
- [mypy: the `deprecated` error code](https://mypy.readthedocs.io/en/stable/error_code_list2.html)
- [pytest: how to capture warnings](https://docs.pytest.org/en/stable/how-to/capture-warnings.html)
- [NEP 23 – Backwards compatibility and deprecation policy](https://numpy.org/neps/nep-0023-backwards-compatibility.html)
- [PDEP-17 – Backwards compatibility and deprecation policy](https://pandas.pydata.org/pdeps/0017-backwards-compatibility-and-deprecation-policy.html)
- [Django deprecation timeline](https://docs.djangoproject.com/en/dev/internals/deprecation/)
- [SQLAlchemy 2.0 migration guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [Matplotlib API guidelines](https://matplotlib.org/devdocs/devel/api_changes.html)
- [scikit-learn `deprecated`](https://scikit-learn.org/stable/modules/generated/sklearn.utils.deprecated.html)
- [Pydantic fields: deprecated fields](https://docs.pydantic.dev/latest/concepts/fields/)

[pep 387]: https://peps.python.org/pep-0387/
[pep 562]: https://peps.python.org/pep-0562/
[pep 565]: https://peps.python.org/pep-0565/
[pep 702]: https://peps.python.org/pep-0702/
[numpy]: https://numpy.org/neps/nep-0023-backwards-compatibility.html
[pandas]: https://pandas.pydata.org/pdeps/0017-backwards-compatibility-and-deprecation-policy.html
[django]: https://docs.djangoproject.com/en/dev/internals/deprecation/
[sqlalchemy]: https://docs.sqlalchemy.org/en/20/changelog/migration_20.html
[matplotlib]: https://matplotlib.org/devdocs/devel/api_changes.html
[scikit-learn]: https://scikit-learn.org/stable/modules/generated/sklearn.utils.deprecated.html
[pydantic]: https://docs.pydantic.dev/latest/concepts/fields/
