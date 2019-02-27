=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. note::

    The library **"Python-Deprecated"** was renamed **"Deprecated"**, simply!
    This project is more consistent because now, the name of the library is the same as the name of the Python package.

    - In your ``setup.py``, you can replace the "Python-Deprecated" dependency with "Deprecated".
    - In your source code, nothing has changed, you will always use ``import deprecated``, as before.
    - I decided to keep the same version number because there is really no change in the source code
      (only in comment or documentation).


v1.1.5 (unreleased)
===================

Bug fix release

Fix
---

- Fix #6: Use :func:`inspect.isroutine` to check if the wrapped object is a user-defined or built-in function or method.

Other
-----

- Upgrade Tox configuration to add support for Python 3.7.
  Also, fix PyTest version for Python 2.7 and 3.4 (limited support).
  Remove dependency 'requests[security]': useless to build documentation.

- Upgrade project configuration (``setup.py``) to add support for Python 3.7.


v1.1.4 (2018-11-03)
===================

Bug fix release

Fix
---

- Fix #4: Correct the function :funct:`~deprecated.deprecated`:
  Don't pass arguments to :meth:`object.__new__` (other than *cls*).

Other
-----

- Change the configuration for TravisCI and AppVeyor:
  drop configuration for Python **2.6** and **3.3**.
  add configuration for Python **3.7**.

  .. note::

     Deprecated is no more tested with Python **2.6** and **3.3**.
     Those Python versions are EOL for some time now and incur incompatibilities
     with Continuous Integration tools like TravisCI and AppVeyor.
     However, this library should still work perfectly...


v1.1.3 (2018-09-03)
===================

Bug fix release

Fix
---

- Fix #2: a deprecated class is a class (not a function). Any subclass of a deprecated class is also deprecated.


v1.1.2 (2018-08-27)
===================

Bug fix release

Fix
---

- Add a ``MANIFEST.in`` file to package additional files like "LICENSE.rst" in the source distribution.


v1.1.1 (2018-04-02)
===================

Bug fix release

Fix
---

- Minor correction in ``CONTRIBUTING.rst`` for Sphinx builds: add the ``-d`` option to put apart the ``doctrees``
  from the generated documentation and avoid warnings with epub generator.
- Fix in documentation configuration: remove hyphens in ``epub_identifier`` (ISBN number has no hyphens).
- Fix in Tox configuration: set the versions interval of each dependency.

Other
-----

- Change in documentation: improve sentence phrasing in the Tutorial.
- Restore the epub title to "Python Deprecated Library v1.1 Documentation" (required for Lulu.com).


v1.1.0 (2017-11-06)
===================

Minor release

Added
-----

- Change in :func:`deprecated.deprecated` decorator: you can give a "reason" message
  to help the developer choose another class, function or method.
- Add support for Universal Wheel (Python versions 2.6, 2.7, 3.3, 3.4, 3.5, 3.6 and PyPy).
- Add missing ``__doc__`` and ``__version__`` attributes to :mod:`deprecated` module.
- Add an extensive documentation of Deprecated Library.

Other
-----

- Improve `Travis <https://travis-ci.org/>`_ configuration file (compatibility from Python 2.6 to 3.7-dev, and PyPy).
- Add `AppVeyor <https://www.appveyor.com/docs/>`_ configuration file.
- Add `Tox <https://tox.readthedocs.io/en/latest/>`_ configuration file.
- Add `BumpVersion <https://github.com/peritus/bumpversion>`_ configuration file.
- Improve project settings: add a long description for the project.
  Set the **license** and the **development status** in the classifiers property.
- Add the :file:`CONTRIBUTING.rst` file: "How to contribute to Deprecated Library".


v1.0.0 (2016-08-30)
===================

Major release

Added
-----

- **deprecated**: Created **@deprecated** decorator
