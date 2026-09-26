# Changelog 1.1.x and 1.0.x

All notable changes for the 1.1.x and 1.0.x releases.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.1.5 (2019-02-28)

Bug fix release

### Fix

- Fix #6: Use [`inspect.isroutine()`](https://docs.python.org/3/library/inspect.html#inspect.isroutine) to check if the wrapped object is a user-defined or built-in function or method.

### Other

- Upgrade Tox configuration to add support for Python 3.7.
  Also, fix PyTest version for Python 2.7 and 3.4 (limited support).
  Remove dependency 'requests[security]': useless to build documentation.
- Upgrade project configuration (`setup.py`) to add support for Python 3.7.

## v1.1.4 (2018-11-03)

Bug fix release

### Fix

- Fix #4: Correct the function [`deprecated()`](https://deprecated.readthedocs.io/en/latest/api.html#deprecated.deprecated):
  Don't pass arguments to [`object.__new__()`](https://docs.python.org/3/reference/datamodel.html#object.__new__) (other than *cls*).

### Other

- Change the configuration for TravisCI and AppVeyor:
  drop configuration for Python **2.6** and **3.3**.
  add configuration for Python **3.7**.

  > [!NOTE]
  > Deprecated is no more tested with Python **2.6** and **3.3**.
  > Those Python versions are EOL for some time now and incur incompatibilities
  > with Continuous Integration tools like TravisCI and AppVeyor.
  > However, this library should still work perfectly...

## v1.1.3 (2018-09-03)

Bug fix release

### Fix

- Fix #2: a deprecated class is a class (not a function). Any subclass of a deprecated class is also deprecated.

## v1.1.2 (2018-08-27)

Bug fix release

### Fix

- Add a `MANIFEST.in` file to package additional files like "LICENSE.rst" in the source distribution.

## v1.1.1 (2018-04-02)

Bug fix release

### Fix

- Minor correction in `CONTRIBUTING.rst` for Sphinx builds: add the `-d` option to put apart the `doctrees`
  from the generated documentation and avoid warnings with epub generator.
- Fix in documentation configuration: remove hyphens in `epub_identifier` (ISBN number has no hyphens).
- Fix in Tox configuration: set the versions interval of each dependency.

### Other

- Change in documentation: improve sentence phrasing in the Tutorial.
- Restore the epub title to "Python Deprecated Library v1.1 Documentation" (required for Lulu.com).

## v1.1.0 (2017-11-06)

Minor release

### Added

- Change in [`deprecated.deprecated()`](https://deprecated.readthedocs.io/en/latest/api.html#deprecated.deprecated) decorator: you can give a "reason" message
  to help the developer choose another class, function or method.
- Add support for Universal Wheel (Python versions 2.6, 2.7, 3.3, 3.4, 3.5, 3.6 and PyPy).
- Add missing `__doc__` and `__version__` attributes to [`deprecated`](https://deprecated.readthedocs.io/en/latest/api.html#module-deprecated) module.
- Add an extensive documentation of Deprecated Library.

### Other

- Improve [Travis](https://www.travis-ci.com/) configuration file (compatibility from Python 2.6 to 3.7-dev, and PyPy).
- Add [AppVeyor](https://www.appveyor.com/docs/) configuration file.
- Add [Tox](https://tox.readthedocs.io/en/latest/) configuration file.
- Add [BumpVersion](https://github.com/peritus/bumpversion) configuration file.
- Improve project settings: add a long description for the project.
  Set the **license** and the **development status** in the classifiers property.
- Add the `CONTRIBUTING.rst` file: "How to contribute to Deprecated Library".

## v1.0.0 (2016-08-30)

Major release

### Added

- **deprecated**: Created **@deprecated** decorator
