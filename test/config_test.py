"""
config_test.py
--------------

Test local config files.

"""

import os
import pytest


@pytest.mark.isolated
def test_local_override():
    """Test whether a local file overrides default options."""
    config_filename = 'decu.cfg'
    assert config_filename not in os.listdir()

    new_opt = '${time}.log'
    config = '[Script]\nlog_file = {}'.format(new_opt)
    with open(config_filename, 'w+') as cfg_file:
        cfg_file.write(config)

    try:
        import decu
        assert decu.config['Script']['log_file'] == new_opt

    finally:
        os.remove(config_filename)
