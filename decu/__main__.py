"""
__main__.py
-----------

decu console commands.

"""

import os
import sys
import decu
from importlib import import_module


def _extract_script_class(module):
    """Return the subclass of decu.Script found in module."""
    for obj in module.__dict__.values():
        if isinstance(obj, type) and decu.Script in obj.__bases__:
            return obj


def exec_script(files):
    """Execute the main function inside each file."""
    import logging

    for file in files:
        module_path, module_file = os.path.split(file)
        module_name, _ = os.path.splitext(module_file)
        project_dir, _ = os.path.split(module_path)
        sys.path.append(os.path.abspath(module_path))

        module = import_module(module_name)
        script = _extract_script_class(module)(project_dir, module_file)
        script.main()
        logger = logging.getLogger()
        for handler in logger.handlers[:]:
            handler.flush()
            logger.removeHandler(handler)


def init(directory):
    """Initialize the directory for a decu project."""
    mkdir = lambda name: os.makedirs(os.path.join(directory, name), exist_ok=True)
    for dir_name in [key for key in decu.config['Script'] if key.endswith('_dir')]:
        mkdir(decu.config['Script'][dir_name])
    print('Initialized empty decu project directory in {}'.format(directory))


def _parse_inspect_opts(opts):
    """Parse the remainder of the options given to decu inspect."""
    if len(opts) % 2 != 0:
        print('additional options need to come in pairs')
        sys.exit(2)
    return {name.strip('-'): path for name, path in
            [opts[i:i + 2] for i in range(0, len(opts), 2)]}


def inspect(files, **kwargs):
    """Load a result file and go into ipython."""
    import re
    from string import Template
    from subprocess import call
    from tempfile import NamedTemporaryFile

    path = files[0]
    scr_cfg = decu.config['Script']
    ins_cfg = decu.config['inspect']
    _, filename = os.path.split(path)
    search = re.sub(r'\$\{.*?\}', '(.*?)', re.sub('\.', '\.', scr_cfg['result_file']))
    search = r'^{}$'.format(search)
    script_name = re.match(search, filename).group(2)

    sys.path.append(scr_cfg['scripts_dir'])
    module = import_module(script_name)
    _class = _extract_script_class(module)

    py_cmd = Template(ins_cfg['py_cmd']).safe_substitute(
        dir=scr_cfg['scripts_dir'].strip('/'), script=script_name,
        cls=_class.__name__, cwd=os.getcwd(), files=files)
    py_cmd_noshow = Template(ins_cfg['py_cmd_noshow']).safe_substitute(
        dir=scr_cfg['scripts_dir'].strip('/'), script=script_name,
        cls=_class.__name__, cwd=os.getcwd(), files=files)
    py_cmd_full = '\n'.join([py_cmd, py_cmd_noshow] +
                            ['{} = np.loadtxt("{}")'.format(name, path)
                             for name, path in kwargs.items()])

    cli_cmd_opts = ['--no-banner']
    # if figure is not None:
    #     py_cmd_full += '\nscript.{}(np.arange(5), result)\n'.format(figure)
    # else:
    #     cli_cmd_opts.append('-i')
    cli_cmd_opts.append('-i')

    py_cmd_show = py_cmd + '\n' + \
        '\n'.join(Template(ins_cfg['noshow_replace']).safe_substitute(var=name)
                  for name in ['result'] + list(kwargs.keys()))
    py_cmd_show = '>>> ' + re.sub(r'\n(.)', r'\n>>> \1', py_cmd_show)
    print(py_cmd_show)

    with NamedTemporaryFile('w+') as tmp:
        tmp.write(py_cmd_full)
        tmp.read()
        cli_cmd = ['ipython', tmp.name] + cli_cmd_opts
        call(cli_cmd)


def main():
    """Execute the script passed as command line argument."""
    import argparse
    parser = argparse.ArgumentParser(description='Experimental computation utilities.')
    subparsers = parser.add_subparsers(help='command', dest='command')

    parser_init = subparsers.add_parser('init', help='initialize a decu '
                                        'project under this directory')

    parser_exec = subparsers.add_parser('exec', help='run a script with decu')
    parser_exec.add_argument('files', nargs='+', help='the script(s) to be run')

    parser_inspect = subparsers.add_parser('inspect', help='inspect results')
    parser_inspect.add_argument('files', nargs='+', help='files to be'
                                'loaded as result')
    parser_inspect.add_argument('opts', nargs=argparse.REMAINDER,
                                help='pairs of name and file paths to read '
                                'as additional variables')
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    elif args.command == 'exec':
        exec_script(args.files)

    elif args.command == 'init':
        init(os.getcwd())

    elif args.command == 'inspect':
        inspect(args.files, **_parse_inspect_opts(args.opts))


if __name__ == "__main__":
    main()
