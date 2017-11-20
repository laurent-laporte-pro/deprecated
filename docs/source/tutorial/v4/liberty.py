# coding: utf-8
""" Liberty library is free """

import pprint

from deprecated import deprecated


@deprecated("This class is not perfect")
class Liberty(object):
    def __init__(self, value):
        self.value = value

    def print_value(self):
        """ Print the value """
        pprint.pprint(self.value)
