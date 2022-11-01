#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides JSON stuff."""

# unused: import geojson
import json


class FileJSON:
    """A class used to represent a JSON File."""

    @staticmethod
    def load_json(path):
        """Load JSON."""
        f = open(path)
        data = json.loads(f.read())
        f.close()
        return data

    # NOTE(SB): indent quadruples file size
    @staticmethod
    def save_dict_to_json(path, dictionary, indent=True):
        """Save dictionary to a JSON file."""
        with open(path, "w") as outfile:
            if indent:
                json.dump(dictionary, outfile, indent=4)
            else:
                json.dump(dictionary, outfile)


def test():
    """Test Function."""
    pass


if __name__ == '__main__':
    """Main"""
    import doctest
    doctest.testmod()
    test()
