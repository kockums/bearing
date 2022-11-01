#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides UUID Class

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
import uuid
# […]

# Import | Libraries
# […]

# Import | Local Modules
# […]


class UUID:
    """
    A class used to represent a UUID

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
    def create_uuid_random():
        """Make a random UUID."""
        id = uuid.uuid4()
        return id

    @staticmethod
    def create_uuid_hex():
        """Convert a UUID to a string of hex digits in standard form."""
        id = str(uuid.uuid4())
        return id

    @staticmethod
    def create_uuid_hex32():
        """Convert a UUID to a string of hex digits in standard form."""
        id = uuid.uuid4().hex
        return id


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
