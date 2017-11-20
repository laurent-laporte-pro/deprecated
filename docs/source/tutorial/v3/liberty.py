# coding: utf-8
""" Liberty library is free """

import pprint

from deprecated import deprecated


class Liberty(object):
    def __init__(self, value):
        self.value = value

    @deprecated("This method is rotten, use 'better_print' instead")
    def print_value(self):
        """ Print the value """
        pprint.pprint(self.value)

    def better_print(self, printer=None):
        """
        Print the value using a *printer*.

        :param printer: Callable used to print the value, by default: :func:`pprint.pprint`
        """
        printer = printer or pprint.pprint
        printer(self.value)
