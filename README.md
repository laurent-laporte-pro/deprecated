# Deprecated Decorator

Python ``@deprecated`` decorator to deprecate old python classes, functions or methods.

[![Build Status](https://travis-ci.org/tantale/deprecated.svg?branch=master)](https://travis-ci.org/tantale/deprecated)
[![Build status](https://ci.appveyor.com/api/projects/status/ctgktcdg2pf8lsxe?svg=true)](https://ci.appveyor.com/project/tantale/deprecated)
[![Coverage Status](https://coveralls.io/repos/github/tantale/deprecated/badge.svg?branch=master)](https://coveralls.io/github/tantale/deprecated?branch=master)
[![GitHub version](https://badge.fury.io/gh/tantale%2Fdeprecated.svg)](https://badge.fury.io/gh/tantale%2Fdeprecated)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/tantale/deprecated/master/LICENSE)
[![Documentation Status](http://readthedocs.org/projects/deprecated/badge/?version=latest)](http://deprecated.readthedocs.io/en/latest/?badge=latest)

## Installation

```shell
pip install Deprecated
```

## Classic usage

To use this, decorate your deprecated function with **@deprecated** decorator:

```python
from deprecated import deprecated


@deprecated
def some_old_function(x, y):
    return x + y
```

You can also decorate a class or a method:

```python
from deprecated import deprecated


class SomeClass(object):
    @deprecated
    def some_old_method(self, x, y):
        return x + y


@deprecated
class SomeOldClass(object):
    pass
```

You can give a "reason" message to help the developer to choose another function/class:

```python
from deprecated import deprecated


@deprecated(reason="use another function")
def some_old_function(x, y):
    return x + y
```

## Sphinx directives

Have you ever wonder how to document that some functions, classes, methods, etc. are deprecated?
This is now possible with the integrated [Sphinx directives](http://www.sphinx-doc.org/en/stable/markup/para.html#directive-versionadded):

```python

from deprecated.sphinx import deprecated
from deprecated.sphinx import versionadded
from deprecated.sphinx import versionchanged


@versionadded(version='1.0', reason="This function is new")
def function_one():
    '''This is the function one'''


@versionchanged(version='1.0', reason="This function is modified")
def function_two():
    '''This is the function two'''


@deprecated(version='1.0', reason="This function will be removed soon")
def function_three():
    '''This is the function three'''

```

## Authors

The authors of this library are:
[Marcos CARDOSO](https://github.com/tantale), and
[Laurent LAPORTE](https://github.com/tantale).

The original code was made in [this StackOverflow post](https://stackoverflow.com/questions/2536307) by
[Leandro REGUEIRO](https://stackoverflow.com/users/1336250/leandro-regueiro),
[Patrizio BERTONI](https://stackoverflow.com/users/1315480/patrizio-bertoni), and
[Eric WIESER](https://stackoverflow.com/users/102441/eric).
