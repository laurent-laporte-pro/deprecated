# coding: utf-8
import pkg_resources

import deprecat


def test_deprecat_has_docstring():
    # The deprecat package must have a docstring
    assert deprecat.__doc__ is not None
    assert "deprecat Library" in deprecat.__doc__


def test_deprecat_has_version():
    # The deprecat package must have a valid version number
    assert deprecat.__version__ is not None
    version = pkg_resources.parse_version(deprecat.__version__)

    assert 'Legacy' not in version.__class__.__name__
