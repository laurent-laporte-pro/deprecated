"""
Deprecated Library
==================

Python ``@deprecated`` decorator to deprecate old python classes, functions or methods.

"""

__version__ = "3.0.0"
__author__ = "Laurent LAPORTE <laurent.laporte.pro@gmail.com>"
__date__ = "2025-10-30"
__credits__ = "(c) Laurent LAPORTE"

from deprecated.classic import deprecated
from deprecated.params import deprecated_params

__all__ = ["deprecated", "deprecated_params"]
