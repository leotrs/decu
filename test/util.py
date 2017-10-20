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
        self.logs_dir = str(tmpdir.mkdir(cfg['logs_dir']))
        self.figures_dir = str(tmpdir.mkdir(cfg['figures_dir']))
        self.results_dir = str(tmpdir.mkdir(cfg['results_dir']))
        self.scripts_dir = str(tmpdir.mkdir(cfg['scripts_dir']))
        self.gendata_dir = str(tmpdir.mkdir(cfg['gendata_dir']))
        super().__init__(os.getcwd(), __name__)
