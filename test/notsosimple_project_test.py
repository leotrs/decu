"""
notsosimple_project_test.py
---------------------------

Run `decu` on the mock project notsosimple_project.

"""

import os
import decu
import pytest
from subprocess import call
from util import make_teardown_fixture

PROJECT_DIR = 'notsosimple_project/'
teardown = pytest.fixture(scope='module', autouse=True)(
    make_teardown_fixture(PROJECT_DIR))


def test_exec():
    """Test that `decu exec src/script.py` generates the appropriate files."""
    cfg = decu.config['Script']
    call(['decu', 'exec', '{}/script.py'.format(cfg['scripts_dir'])])
    assert os.listdir(decu.config['logging']['logs_dir'])
    assert os.listdir(cfg['figures_dir'])
    assert os.listdir(cfg['results_dir'])
