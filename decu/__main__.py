"""
__main__.py
-----------

Main decu executable.

"""

import os
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
    import sys
    from importlib import import_module
    module_path, module_file = os.path.split(path)
    sys.path.append(make_absolute_path(module_path))
    module_name, _ = os.path.splitext(module_file)
    module = import_module(module_name)
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


def inspect(path):
    """Load a result file and go into ipython."""
    from subprocess import call
    py_cmd = 'import decu;import numpy as np;results = np.loadtxt("{}")'.format(path)
    cli_cmd = ['ipython', '-i', '--no-banner', '-c', '\'{}\''.format(py_cmd)]
    print(py_cmd.replace(';', '\n'))
    call(cli_cmd)


def main():
    """Execute the script passed as command line argument."""
    from argparse import ArgumentParser, ArgumentError
    parser = ArgumentParser(description='Experimental computation utilities.')
    parser.add_argument('mode', choices=['init', 'exec', 'inspect'])
    parser.add_argument('path', nargs='?', help='the script to be run')
    args = parser.parse_args()

    if args.mode == 'exec':
        if args.path is None:
            parser.error('path must be specified when using exec')
        else:
            exec_script(args.path)
    elif args.mode == 'init':
        init(os.getcwd())
    elif args.mode == 'inspect':
        if args.path is None:
            parser.error('path must be specified when using inspect')
        else:
            inspect(args.path)


if __name__ == "__main__":
    main()
