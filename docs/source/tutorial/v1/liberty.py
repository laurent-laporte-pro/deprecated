# coding: utf-8
""" Liberty library is free """

import pprint

from deprecated import deprecated


@deprecated
def print_value(value):
    """
    Print the value

    :param value: The value to print
    """
    pprint.pprint(value)


def better_print(value, printer=None):
    """
    Print the value using a *printer*.

    :param value: The value to print
    :param printer: Callable used to print the value, by default: :func:`pprint.pprint`
    """
    printer = printer or pprint.pprint
    printer(value)
