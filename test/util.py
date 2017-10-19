"""
util.py
-------

Testing utilities.

"""

import os
from decu import Script, config


class TestScript(Script):
    """Script subclass used for testing purposes."""
    def __init__(self, tmpdir):
        cfg = config['Script']
        self.logs_dir = tmpdir.mkdir(cfg['logs_dir']).dirname
        self.figures_dir = tmpdir.mkdir(cfg['figures_dir']).dirname
        self.results_dir = tmpdir.mkdir(cfg['results_dir']).dirname
        self.scripts_dir = tmpdir.mkdir(cfg['scripts_dir']).dirname
        super().__init__(os.getcwd(), __name__)
