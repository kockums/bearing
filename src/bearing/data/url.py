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
    """"""

    # Static Methods

    @staticmethod
    def is_string_an_url(url_string: str) -> bool:
        result = validators.url(url_string)

        if isinstance(result, ValidationFailure):
            return False

        return result


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











