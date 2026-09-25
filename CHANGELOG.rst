===============
Changelog 1.3.x
===============

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


Unreleased
==========

Python 3.12+ modernization

.. warning::

    This release drops the support of Python 2.7 and of Python 3 versions older than 3.12.
    Use Deprecated 1.3.x on these versions.

Changed
-------

- Require Python >= 3.12 and wrapt >= 1.16 (first wrapt release supporting Python 3.12).
- Remove the ``inspect2`` dependency (it was only used on Python 2).
- Remove the Python 2 compatibility constructs (``u""`` literals, ``coding`` cookies,
  ``class Foo(object)``, ``super(Class, self)``, ``OrderedDict``...).
- Remove the undocumented ``deprecated.classic.string_types`` compatibility tuple.
  A ``bytes`` positional *reason* is still accepted by ``@deprecated``, as before.
- Migrate the packaging from setuptools (``setup.py``/``setup.cfg``/``MANIFEST.in``) to
  ``pyproject.toml`` with the Hatchling build backend; the version is read from
  ``deprecated/__init__.py``.
- Manage the project with uv (``uv.lock``) and replace tox by the ``hatch test`` matrix.
- Update the Fedora RPM spec file to the ``%pyproject_*`` macros.

Added
-----

- Add Python 3.12 type annotations to the public API and ship the ``py.typed`` marker (PEP 561):
  the decorators preserve the signature of the decorated functions and classes.
- Add the ``hatch check code`` (Ruff lint), ``hatch check fmt`` (Ruff format)
  and ``hatch check types`` (mypy, strict mode) quality checks.
- Add non-regression tests for the behaviours which differ between Python 2 and Python 3.

Other
-----

- Run the CI with uv and Hatch on Python 3.12, 3.13 and 3.14 (Linux, macOS and Windows),
  plus the wrapt compatibility matrix.


v1.3.1 (2025-10-30)
===================

Patch release: Packaging fix

Fixed
-----

- Restore missing source distribution (``.tar.gz``) that was not included in v1.3.0.


v1.3.0 (2025-10-29)
===================

.. note::

    This release was **yanked** on PyPI due to a missing source distribution (``.tar.gz``).
    See issue #94: https://github.com/laurent-laporte-pro/deprecated/issues/94
    It has been replaced by version 1.3.1.

Minor release: Parameters deprecation

Added
-----

- Add compatibility tests and adjustments for Wrapt v2.0. See PR #88 (musicinmybrain).

- Add experimental `@deprecated_params` decorator to mark function parameters as deprecated at call-time; emits warnings when deprecated parameters are used with optional messages and configurable warning categories. See PR #93.

Documentation
-------------

- Update the Wrapt compatibility matrix to include Python 3.13 and 3.14. See PR #91

Changed
-------

- Limit test coverage collection to the dedicated ``coverage`` tox environment to avoid collecting coverage across all test environments and reduce cross-environment coverage noise. See PR #92.
