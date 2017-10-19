"""
console_test.py
---------------

Test the console scripts.

"""

import pytest
import decu
import decu.__main__ as main
from subprocess import check_call, CalledProcessError


def test_init(tmpdir):
    """Test the `decu init` command."""
    dir_names = [tmpdir.join(v) for k, v in decu.config['Script'].items()
                 if k.endswith('_dir')]
    for name in dir_names:
        assert name not in tmpdir.listdir()
    main.init(str(tmpdir))
    for name in dir_names:
        assert name in tmpdir.listdir()


def test_exec_no_arg():
    """Test that `decu exec` without an argument gives an error."""
    # Error code 2 means 'misuse of shell built-ins' and is the code that
    # argparse gives in case there's an parsing error.
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'exec'])


def test_inspect_no_arg():
    """Test that `decu inspect` without an argument gives an error."""
    # Error code 2 means 'misuse of shell built-ins' and is the code that
    # argparse gives in case there's an parsing error.
    with pytest.raises(CalledProcessError):
        check_call(['decu', 'inspect'])
