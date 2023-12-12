# -*- coding: utf-8 -*-


"""
Provides a Bearing entry point.

"""


# Import | Futures
from __future__ import print_function

# Import | Standard Library
import platform
try:
    import pkg_resources
except ImportError:
    pkg_resources = None

# Import | Libraries
import bearing

# Import | Local Modules


if __name__ == "__main__":

    print()
    print("Bearings are set!")
    print()
    print("Bearing: {}".format(bearing.__version__))
    print("Python: {} ({})".format(
        platform.python_version(),
        platform.python_implementation())
    )

    if pkg_resources:
        working_set = pkg_resources.working_set
        packages = set(
            [p.project_name for p in working_set]
        ) - set(["Bearing"])

        bearing_pkgs = [
            p for p in packages if p.lower().startswith("bearing")
        ]

        if bearing_pkgs:
            print("Extensions: {}".format([p for p in bearing_pkgs]))
