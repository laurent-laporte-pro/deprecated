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


v1.2.14 (unreleased)
====================

Bug fix release

Fix
---

- Fix #60: return a correctly dedented docstring when long docstring are using the D212 or D213 format.


v1.2.13 (2021-09-05)
====================

Bug fix release

Fix
---

- Fix #45: Change the signature of the :func:`~deprecated.sphinx.deprecated` decorator to reflect
  the valid use cases.

- Fix #48: Fix ``versionadded`` and ``versionchanged`` decorators: do not return a decorator factory,
  but a Wrapt adapter.

Other
-----

- Fix configuration for AppVeyor: simplify the test scripts and set the version format to match the current version.

- Change configuration for Tox:

  + change the requirements for ``pip`` to "pip >= 9.0.3, < 21" (Python 2.7, 3.4 and 3.5).
  + install ``typing`` when building on Python 3.4 (required by Pytest->Attrs).
  + run unit tests on Wrapt 1.13 (release candidate).

- Migrating project to `travis-ci.com <https://travis-ci.com/github/tantale/deprecated>`_.


v1.2.12 (2021-03-13)
====================

Bug fix release

Fix
---

- Avoid "Explicit markup ends without a blank line" when the decorated function has no docstring.

- Fix #40: 'version' argument is required in Sphinx directives.

- Fix #41: :mod:`deprecated.sphinx`: strip Sphinx cross-referencing syntax from warning message.


Other
-----

- Change in Tox and Travis CI configurations: enable unit testing on Python 3.10.


v1.2.11 (2021-01-17)
====================

Bug fix release

Fix
---

- Fix packit configuration: use ``upstream_tag_template: v{version}``.

- Fix #33: Change the class :class:`~deprecated.sphinx.SphinxAdapter`:
  add the ``line_length`` keyword argument to the constructor to specify the max line length of the directive text.
  Sphinx decorators also accept the ``line_length`` argument.

- Fix #34: ``versionadded`` and ``versionchanged`` decorators don't emit ``DeprecationWarning``
  anymore on decorated classes.


Other
-----

- Change the Tox configuration to run tests on Python 2.7, Python 3.4 and above (and PyPy 2.7 & 3.6).

- Update the classifiers in ``setup.py``.

- Replace ``bumpversion`` by `bump2version <https://pypi.org/project/bump2version/>`_ in ``setup.py`` and documentation.

- Update configuration for Black and iSort.

- Fix the development requirement versions in ``setup.py`` for Python 2.7 EOL.


v1.2.10 (2020-05-13)
====================

Bug fix release

Fix
---

- Fix #25: ``@deprecated`` respects global warning filters with actions other than "ignore" and "always" on Python 3.

Other
-----

- Change the configuration for TravisCI to build on pypy and pypy3.

- Change the configuration for TravisCI and AppVeyor: drop configuration for Python **3.4** and add **3.8**.


v1.2.9 (2020-04-10)
===================

Bug fix release

Fix
---

- Fix #20: Set the :func:`warnings.warn` stacklevel to 2 if the Python implementation is `PyPy <https://www.pypy.org/>`_.

- Fix packit configuration: use ``dist-git-branch: fedora-all``.

Other
-----

- Change the Tox configuration to run tests on PyPy v2.7 and 3.6.


v1.2.8 (2020-04-05)
===================

Bug fix release

Fix
---

- Fix #15: The ``@deprecated`` decorator doesn't set a warning filter if the *action* keyword argument is
  not provided or ``None``. In consequences, the warning messages are only emitted if the global filter allow it.
  For more information, see `The Warning Filter <https://docs.python.org/3/library/warnings.html#the-warnings-filter>`_
  in the Python documentation.

- Fix #13: Warning displays the correct filename and line number when decorating a class if wrapt
  does not have the compiled c extension.

Documentation
-------------

- The :ref:`api` documentation and the :ref:`tutorial` is improved to explain how to use
  custom warning categories and local filtering (warning filtering at function call).

- Fix #17: Customize the sidebar to add links to the documentation to the source in GitHub and to the Bug tracker.
  Add a logo in the sidebar and change the logo in the main page to see the library version.

- Add a detailed documentation about :ref:`sphinx_deco`.


Other
-----

- Change the Tox configuration to test the library with Wrapt 1.12.x.


v1.2.7 (2019-11-11)
===================

Bug fix release

Fix
---

- Fix #13: Warning displays the correct filename and line number when decorating a function if wrapt
  does not have the compiled c extension.

Other
-----

- Support packit for Pull Request tests and sync to Fedora (thanks to Petr Hráček).
  Supported since v1.2.6.

- Add `Black <https://black.readthedocs.io/en/latest/>`_ configuration file.


v1.2.6 (2019-07-06)
===================

Bug fix release

Fix
---

- Fix #9: Change the project's configuration: reinforce the constraint to the Wrapt requirement.

Other
-----

- Upgrade project configuration (``setup.py``) to add the *project_urls* property:
  Documentation, Source and Bug Tracker URLs.

- Change the Tox configuration to test the library against different Wrapt versions.

- Fix an issue with the AppVeyor build: upgrade setuptools version in ``appveyor.yml``,
  change the Tox configuration: set ``py27,py34,py35: pip >= 9.0.3, < 19.2``.


v1.2.5 (2019-02-28)
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


v1.2.4 (2018-11-03)
===================

Bug fix release

Fix
---

- Fix #4: Correct the class :class:`~deprecated.classic.ClassicAdapter`:
  Don't pass arguments to :meth:`object.__new__` (other than *cls*).

Other
-----

- Add missing docstring to the classes :class:`~deprecated.classic.ClassicAdapter`
  and :class:`~deprecated.sphinx.SphinxAdapter`.

- Change the configuration for TravisCI and AppVeyor:
  drop configuration for Python **2.6** and **3.3**.
  add configuration for Python **3.7** (if available).

  .. note::

     Deprecated is no more tested with Python **2.6** and **3.3**.
     Those Python versions are EOL for some time now and incur incompatibilities
     with Continuous Integration tools like TravisCI and AppVeyor.
     However, this library should still work perfectly...


v1.2.3 (2018-09-12)
===================

Bug fix release

Fix
---

- Fix #3: ``deprecated.sphinx`` decorators don't update the docstring.


v1.2.2 (2018-09-04)
===================

Bug fix release

Fix
---

- Fix #2: a deprecated class is a class (not a function). Any subclass of a deprecated class is also deprecated.

- Minor fix: add missing documentation in :mod:`deprecated.sphinx` module.


v1.2.1 (2018-08-27)
===================

Bug fix release

Fix
---

- Add a ``MANIFEST.in`` file to package additional files like "LICENSE.rst" in the source distribution.


v1.2.0 (2018-04-02)
===================

Minor release

Added
-----

- Add decorators for Sphinx directive integration: ``versionadded``, ``versionchanged``, ``deprecated``.
  That way, the developer can document the changes.

Changed
-------

- Add the ``version`` parameter to the ``@deprecated`` decorator:
  used to specify the starting version number of the deprecation.
- Add a way to choose a ``DeprecationWarning`` subclass.

Removed
-------

- Deprecated no longer supports Python **2.6** and **3.3**. Those Python versions
  are EOL for some time now and incur maintenance and compatibility costs on
  the Deprecated core team, and following up with the rest of the community we
  decided that they will no longer be supported starting on this version. Users
  which still require those versions should pin Deprecated to ``< 1.2``.


v1.1.5 (2019-02-28)
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

- Fix #4: Correct the function :func:`~deprecated.deprecated`:
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

- Improve `Travis <https://travis-ci.com/>`_ configuration file (compatibility from Python 2.6 to 3.7-dev, and PyPy).
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
