"""
__main__.py
-----------

Main decu executable.

"""

import os
import decu
from importlib import import_module
from string import Template


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
    module_path, module_file = os.path.split(path)
    sys.path.append(make_absolute_path(module_path))
    module_name, _ = os.path.splitext(module_file)
    module = import_module(module_name)
    script = extract_script_class(module)(os.getcwd(), module_file)
    script.main()


def init(path):
    """Initialize the path for a decu project."""
    from os.path import join
    mkdir = lambda name: os.makedirs(join(path, name), exist_ok=True)
    mkdir(decu.config['Script']['data_dir'])
    mkdir(decu.config['Script']['logs_dir'])
    mkdir(decu.config['Script']['results_dir'])
    mkdir(decu.config['Script']['figures_dir'])
    mkdir(decu.config['Script']['scripts_dir'])
    print('Initialized empty decu project directory in {}'.format(path))


def inspect(path, figure=None):
    """Load a result file and go into ipython."""
    import re
    import sys
    from tempfile import NamedTemporaryFile
    from subprocess import call

    cfg = decu.config['Script']
    _, filename = os.path.split(path)
    search = re.sub(r'\$\{.*?\}', '(.*?)', re.sub('\.', '\.', cfg['result_file']))
    search = r'^{}$'.format(search)
    script_name = re.match(search, filename).group(2)

    sys.path.append(cfg['scripts_dir'])
    module = import_module(script_name)
    _class = extract_script_class(module)

    py_cmd = Template(decu.config['inspect']['py_cmd']).safe_substitute(
        dir=cfg['scripts_dir'].strip('/'), script=script_name,
        cls=_class.__name__, cwd=os.getcwd(), path=path)

    cli_cmd_opts = ['--no-banner']
    if figure is not None:
        py_cmd += '\nscript.{}(np.arange(5), result)\n'.format(figure)
    else:
        cli_cmd_opts.append('-i')

    print(py_cmd)
    with NamedTemporaryFile('w+') as tmp:
        tmp.write(py_cmd)
        tmp.read()
        cli_cmd = ['ipython', tmp.name] + cli_cmd_opts
        call(cli_cmd)


def main():
    """Execute the script passed as command line argument."""
    from argparse import ArgumentParser, ArgumentError
    parser = ArgumentParser(description='Experimental computation utilities.')
    parser.add_argument('mode', choices=['init', 'exec', 'inspect'])
    parser.add_argument('path', nargs='?', help='the script to be run')
    parser.add_argument('-p', '--plot', help='if using inspect, the '
                        '@figure method to call on the inspected result')
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
            inspect(args.path, figure=args.plot)


if __name__ == "__main__":
    main()
