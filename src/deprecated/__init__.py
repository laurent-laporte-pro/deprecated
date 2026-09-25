"""
Deprecated Library
==================

Python ``@deprecated`` decorator to deprecate old python classes, functions or methods.

"""

#: Single source of the version, updated with `hatch version <major|minor|patch>`.
__version__ = "3.0.0"
__author__ = "Laurent LAPORTE <laurent.laporte.pro@gmail.com>"
__credits__ = "(c) Laurent LAPORTE"

from deprecated.classic import deprecated
from deprecated.params import deprecated_params

__all__ = ["deprecated", "deprecated_params"]
