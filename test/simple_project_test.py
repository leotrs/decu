"""
simple_project_test.py
----------------------

Run `decu` on the mock project simple_project.

"""

import os
import decu
import pytest
from decu import __main__ as main

PROJECT_DIR = 'simple_project/'


# Finalization code. See
# docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
@pytest.fixture(scope='module', autouse=True)
def teardown():
    """Guarantee a clean slate before and after all tests in this module."""
    def clean_up():
        """Delete all files except for scripts."""
        dir_names = [v for k, v in decu.config['Script'].items()
                     if k.endswith('_dir')]
        dir_names.remove(decu.config['Script']['scripts_dir'])
        for dir_name in [d for d in dir_names if d in os.listdir(PROJECT_DIR)]:
            for file in os.listdir(os.path.join(PROJECT_DIR, dir_name)):
                os.remove(os.path.join(PROJECT_DIR, dir_name, file))

    clean_up()
    os.chdir(PROJECT_DIR)
    yield None
    os.chdir('..')
    clean_up()


@pytest.mark.isolated
def test_exec_multiple_args(tmpdir):
    """`decu exec` on two equal scripts should generate two equal log files.

    This is a randomized test. The log files will be equal, except for the
    time stamps and the elapsed time, and these two times will change every
    time we run the test suite. What we really check is that the logs are
    within a percentage similarity of each other.

    """
    from difflib import SequenceMatcher

    main.exec_script(['src/script1.py', 'src/script2.py'])
    log_dir = decu.config['Script']['logs_dir']
    assert len(os.listdir(log_dir)) == 2

    logs = []
    for log_file in os.listdir(log_dir):
        with open(os.path.join(log_dir, log_file)) as file:
            logs.append(file.read())
    differ = SequenceMatcher(a=logs[0], b=logs[1])
    assert differ.ratio() > 0.85
