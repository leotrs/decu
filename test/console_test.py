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


def test_inspect_wrong_args():
    """`decu inspect` with wrong arguments should give an error."""
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect'])
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', 'testscript/src/testscript.py', '--plot'])
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', 'testscript/src/testscript.py', '--data'])
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect', 'testscript/src/testscript.py', '--data', 'foo', '--bar'])
