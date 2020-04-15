__version__ = "0.0.1"

import os
import sys


def get_airtest_version():
    pip_pkg_dir = os.path.join(os.path.dirname(__file__), "..", "..")
    pip_pkg_dir = os.path.abspath(pip_pkg_dir)

    from airtest.utils.version import __version__ as airtest_version
    return (
        'airrun {} with [airtest {}] from {} (python {})'.format(
            __version__, airtest_version, pip_pkg_dir, sys.version[:3],
        )
    )


def show_version():
    sys.stdout.write(get_airtest_version())
    sys.stdout.write(os.linesep)
    sys.exit()
