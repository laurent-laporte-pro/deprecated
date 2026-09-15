# coding: utf-8
from packaging.version import Version

import deprecated


def test_deprecated_has_docstring():
    # The deprecated package must have a docstring
    assert deprecated.__doc__ is not None
    assert "Deprecated Library" in deprecated.__doc__


def test_deprecated_has_version():
    # The deprecated package must have a valid version number
    assert deprecated.__version__ is not None

    try:
        Version(deprecated.__version__)
        valid_version = True
    except packaging.version.InvalidVersion:
        valid_version = False

    assert valid_version is True
