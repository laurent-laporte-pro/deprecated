# coding: utf-8
from deprecated.sphinx import deprecated


@deprecated(version="0.2.3",
            reason="The *i* parameter is deprecated, "
                   "you may consider using *increment* instead.")
def my_add(x, i=None, increment=0):
    """
    This function adds *x* and *increment*.

    :param x: The *x* value.
    :param i: *i* parameter is deprecated, use *increment* instead.
    :param increment: The increment value.
    :return: sum of *x* and *increment*.
    """
    increment = increment if i is None else i
    return x + increment


print(my_add.__doc__)
