def mean(values):
    """
    Compute the arithmetic mean (“average”) of values.

    :type  values: list[float]
    :param values: List of floats
    :return: Mean of values.

    .. deprecated:: 2.5.0
       Since Python 3.4, you can use the standard function :func:`statistics.mean`.
    """
    return sum(values) / len(values)
