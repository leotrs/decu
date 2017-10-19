"""
__main__.py
-----------

Main decu executable.

"""

import os
import sys
import importlib
import decu
from datetime import datetime
NOW = datetime.now()


def make_absolute_path(path):
    """Return the absolute path."""
    if not os.path.isabs(path):
        return os.path.join(os.getcwd(), path)
    return path


def extract_script_class(module):
    """Return the subclass of decu.Script found in module."""
    for obj in module.__dict__.values():
        if isinstance(obj, type) and decu.Script in obj.__bases__:
            return obj


def exec_script(path):
    """Execute the main function inside a file."""
    module_path, module_file = os.path.split(path)
    sys.path.append(make_absolute_path(module_path))
    module_name, _ = os.path.splitext(module_file)
    module = importlib.import_module(module_name)
    script = extract_script_class(module)(NOW, os.getcwd(), module_file)
    script.main()


def init(path):
    """Initialize the path for a decu project."""
    from os.path import join
    mkdir = lambda name: os.makedirs(join(path, name), exist_ok=True)
    mkdir(decu.config['Script']['data_dir'])
    mkdir(decu.config['Script']['logs_dir'])
    mkdir(decu.config['Script']['results_dir'])
    mkdir(decu.config['Script']['figures_dir'])
    print('Initialized empty decu project directory in {}'.format(path))


def main():
    """Execute the script passed as command line argument."""
    from argparse import ArgumentParser, ArgumentError
    parser = ArgumentParser(description='Experimental computation utilities.')
    parser.add_argument('mode', choices=['init', 'exec'])
    parser.add_argument('path', nargs='?', help='the script to be run')
    args = parser.parse_args()

    if args.mode == 'exec':
        if args.path is None:
            parser.error('path must be specified when using exec')
        else:
            exec_script(args.path)
    elif args.mode == 'init':
        init(os.getcwd())



if __name__ == "__main__":
    main()
