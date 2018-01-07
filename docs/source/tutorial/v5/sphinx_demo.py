# coding: utf-8
from deprecated.sphinx import deprecated
from deprecated.sphinx import versionadded
from deprecated.sphinx import versionchanged


@deprecated(
    reason="""
    This is deprecated, really. So you need to use another function.
    But I don\'t know which one.
    
       - The first,
       - The second.
    
    Just guess!
    """,
    version='0.3.0')
@versionchanged(
    reason='Well, I add a new feature in this function. '
           'It is very useful as you can see in the example below, so try it. '
           'This is a very very very very very long sentence.',
    version='0.2.0')
@versionadded(
    reason='Here is my new function.',
    version='0.1.0')
def successor(n):
    """
    Calculate the successor of a number.

    :param n: a number
    :return: number + 1
    """
    return n + 1


help(successor)
