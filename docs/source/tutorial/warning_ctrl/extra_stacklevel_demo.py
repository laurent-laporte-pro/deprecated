import warnings

from deprecated import deprecated


@deprecated(version='1.0', extra_stacklevel=1)
class MyObject(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "object: {name}".format(name=self.name)


def create_object(name):
    return MyObject(name)


if __name__ == '__main__':
    warnings.filterwarnings("default", category=DeprecationWarning)
    # warn here:
    print(create_object("orange"))
    # and also here:
    print(create_object("banane"))
