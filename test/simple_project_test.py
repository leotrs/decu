"""
simple_project_test.py
----------------------

Run `decu` on the mock project simple_project.

"""

import os
import decu
import pytest
from decu import __main__ as main
from util import make_teardown_fixture

PROJECT_DIR = 'simple_project/'
teardown = pytest.fixture(scope='function', autouse=True)(
    make_teardown_fixture(PROJECT_DIR))


def test_exec_single_arg():
    """`decu exec` should accept one single argument."""
    cfg = decu.config['Script']
    main.exec_script([os.path.join(cfg['scripts_dir'], 'script1.py')])
    assert len(os.listdir(decu.config['logging']['logs_dir'])) == 1
    assert len(os.listdir(cfg['results_dir'])) == 1


def test_exec_multiple_args():
    """`decu exec` on two equal scripts should generate two equal log files.

    This is a randomized test. The log files will be equal, except for the
    time stamps and the elapsed time, and these two times will change every
    time we run the test suite. What we really check is that the logs are
    within a percentage similarity of each other.

    """
    from difflib import SequenceMatcher

    main.exec_script(['src/script1.py', 'src/script2.py'])
    log_dir = decu.config['logging']['logs_dir']
    assert len(os.listdir(log_dir)) == 2
    logs = []
    for log_file in os.listdir(log_dir):
        with open(os.path.join(log_dir, log_file)) as file:
            logs.append(file.read())
    differ = SequenceMatcher(a=logs[0], b=logs[1])
    assert differ.ratio() > 0.85
