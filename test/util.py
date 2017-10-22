"""
util.py
-------

Testing utilities.

"""

import decu


class TestScript(decu.Script):
    """Script subclass used for testing purposes."""
    def __init__(self, tmpdir):
        cfg = decu.config['Script']
        self.logs_dir = str(tmpdir.mkdir(cfg['logs_dir']))
        self.figures_dir = str(tmpdir.mkdir(cfg['figures_dir']))
        self.results_dir = str(tmpdir.mkdir(cfg['results_dir']))
        self.scripts_dir = str(tmpdir.mkdir(cfg['scripts_dir']))
        self.gendata_dir = str(tmpdir.mkdir(cfg['gendata_dir']))
        super().__init__(str(tmpdir), __name__)
