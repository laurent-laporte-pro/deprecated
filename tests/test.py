import importlib.metadata

from packaging.version import Version

import deprecated


def test_deprecated_has_docstring():
    # The deprecated package must have a docstring
    assert deprecated.__doc__ is not None
    assert "Deprecated Library" in deprecated.__doc__


def test_deprecated_has_version():
    # The deprecated package must have a valid (PEP 440) version number:
    # `packaging.version.Version` raises `InvalidVersion` otherwise.
    assert deprecated.__version__ is not None
    version = Version(deprecated.__version__)
    assert str(version) == deprecated.__version__


def test_deprecated_version_matches_distribution_metadata():
    # The version is read by Hatch from `src/deprecated/__init__.py`:
    # the installed distribution metadata must be consistent.
    assert importlib.metadata.version("Deprecated") == deprecated.__version__
