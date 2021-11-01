# coding: utf-8
import pkg_resources

import deprecator


def test_deprecator_has_docstring():
    # The deprecator package must have a docstring
    assert deprecator.__doc__ is not None
    assert "deprecator Library" in deprecator.__doc__


def test_deprecator_has_version():
    # The deprecator package must have a valid version number
    assert deprecator.__version__ is not None
    version = pkg_resources.parse_version(deprecator.__version__)

    assert 'Legacy' not in version.__class__.__name__
