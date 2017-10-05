"""
__main__.py
-----------

Main decu executable.

"""

import os
import sys
import importlib
import decu


def make_absolute_path(path):
    """Return the absolute path."""
    if not os.path.isabs(path):
        return os.path.join(os.getcwd(), path)
    return path


def get_script_class(module):
    """Return a reference to a subclass of decu.Script found in module, if any."""
    for obj in module.__dict__.values():
        if isinstance(obj, type) and decu.Script in obj.__bases__:
                return obj


def main():
    """Execute the script passed as command line argument."""
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Experimental computation utilities.')
    parser.add_argument('file', help='the script to be run')
    args = parser.parse_args()
    module_path, module_file = os.path.split(args.file)

    sys.path.append(make_absolute_path(module_path))
    module_name, _ = os.path.splitext(module_file)

    module = importlib.import_module(module_name)
    script_class = get_script_class(module)
    script = script_class()
    script.main()



if __name__ == "__main__":
    main()
