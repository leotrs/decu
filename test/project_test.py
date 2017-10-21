"""
project_test.py
---------------

Run `decu` on the mock project test_project.

"""

import os
import decu
import pytest
from random import choice
from subprocess import call

PROJECT_DIR = 'test_project/'


# Finalization code. See
# docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
@pytest.fixture(scope='module', autouse=True)
def teardown():
    """Guarantee a clean slate before and after all tests in this module."""
    def clean_up():
        """Delete all files except scripts."""
        dir_names = [v for k, v in decu.config['Script'].items()
                     if k.endswith('_dir')]
        dir_names.remove(decu.config['Script']['scripts_dir'])
        for dir_name in dir_names:
            for file in os.listdir(os.path.join(PROJECT_DIR, dir_name)):
                os.remove(os.path.join(PROJECT_DIR, dir_name, file))

    clean_up()
    os.chdir(PROJECT_DIR)
    yield None
    os.chdir('..')
    clean_up()


def test_exec():
    """Test that `decu exec src/script.py` generates the appropriate files."""
    cfg = decu.config['Script']
    call(['decu', 'exec', '{}/script.py'.format(cfg['scripts_dir'])])
    assert os.listdir(cfg['logs_dir'])
    assert os.listdir(cfg['figures_dir'])
    assert os.listdir(cfg['results_dir'])
