# deprecat Decorator

Python ``@deprecat`` decorator to deprecate old python classes, functions or methods.

## Installation

```shell
pip install deprecat
```

## Usage

To use this, decorate your deprecated function with **@deprecat** decorator:

```python
from deprecat import deprecat


@deprecat
def some_old_function(x, y):
    return x + y
```

You can also decorate a class or a method:

```python
from deprecated import deprecat


class SomeClass(object):
    @deprecat
    def some_old_method(self, x, y):
        return x + y


@deprecat
class SomeOldClass(object):
    pass
```

You can give a "reason" message to help the developer to choose another function/class:

```python
from deprecat import deprecat


@deprecat(reason="use another function")
def some_old_function(x, y):
    return x + y
```

## Authors

The authors of this library are:
[Marcos CARDOSO](https://github.com/vrcmarcos), and
[Laurent LAPORTE](https://github.com/tantale).
The original code was made in [this StackOverflow post](https://stackoverflow.com/questions/2536307) by
[Leandro REGUEIRO](https://stackoverflow.com/users/1336250/leandro-regueiro),
[Patrizio BERTONI](https://stackoverflow.com/users/1315480/patrizio-bertoni), and
[Eric WIESER](https://stackoverflow.com/users/102441/eric).


Modified and now maintained by: [Meenal Jhajharia](https://github.com/mjhajharia) 
