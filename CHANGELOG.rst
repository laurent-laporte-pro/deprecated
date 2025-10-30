===============
Changelog 1.3.x
===============

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


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
