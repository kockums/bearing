#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides File Utils

...

Examples:
    ...

Attributes:
    ...

Todo:

"""


# Import | Futures
# […]

# Import | Standard Library
import re
import unicodedata
# […]

# Import | Libraries
# […]

# Import | Local Modules
# […]


class Slug:
    """
    A class used to represent a Slug

    ...

    Attributes
    ----------


    Methods
    -------
    test()
        test method
    """

    # Static Methods

    @staticmethod
    def create_slug(value, allow_unicode=False):
        """"""
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')

    @staticmethod
    def create_slug_snake(value, allow_unicode=False):
        """"""
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '_', value).strip('-_')


    # Methods | test

    def test_something(self):
        """Test Method"""
        pass


def test():
    """Test Function"""
    pass


if __name__ == '__main__':
    """Main"""
    import doctest
    doctest.testmod()
    test()
