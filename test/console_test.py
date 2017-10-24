"""
console_test.py
---------------

Test the console scripts.

"""

import pytest
from decu import config
from decu import __main__ as main
from subprocess import check_call, CalledProcessError


def test_init(tmpdir):
    """`decu init` should create the appropriate directories."""
    dir_names = [tmpdir.join(v) for k, v in config['Script'].items()
                 if k.endswith('_dir')]
    for name in dir_names:
        assert name not in tmpdir.listdir()
    main.init(str(tmpdir))
    for name in dir_names:
        assert name in tmpdir.listdir()


def test_already_initialized_init(tmpdir):
    """`decu init` on an already initialized project shouldn't harm it."""
    dir_names = [tmpdir.join(v) for k, v in config['Script'].items()
                 if k.endswith('_dir')]
    main.init(str(tmpdir))

    test_dir = tmpdir.join(config['Script']['scripts_dir'])
    test_filename = test_dir.join('foo.txt')
    with test_filename.open('w+') as file:
        file.write('this is a test')

    main.init(str(tmpdir))
    for name in dir_names:
        assert name in tmpdir.listdir()
    assert test_filename in test_dir.listdir()


def test_exec_no_arg():
    """`decu exec` without an argument should give an error."""
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'exec'])


def test_exec_no_class(tmpdir):
    """`decu exec` on a file without a Script class should error out."""
    main.init(str(tmpdir))
    src_dir = config['Script']['scripts_dir']
    filename = tmpdir.join(src_dir, 'empty.py')
    with filename.open('w+') as file:
        file.write('import decu\nclass MyScript():\n    pass')
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', str(filename)])


def test_exec_empty_file(tmpdir):
    """`decu exec` on an empty file should error out."""
    main.init(str(tmpdir))
    src_dir = config['Script']['scripts_dir']
    empty_fn = tmpdir.join(src_dir, 'empty.py')
    empty_fn.open('w+').close()
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', str(empty_fn)])


def test_exec_nonexistent_file():
    import os
    non_existant = 'totally_non_existent_file.abc'
    assert 'totally_non_existent_file.abc' not in os.listdir()
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', non_existant])


def test_inspect_wrong_args():
    """`decu inspect` with wrong arguments should give an error."""
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect'])

    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', 'testscript/src/testscript.py',
                    '--plot'])
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', 'testscript/src/testscript.py',
                    '--data'])
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', 'testscript/src/testscript.py',
                    '--data', 'foo', '--bar'])
