"""
util.py
-------

Testing utilities.

"""

import os
import decu
import datetime

class TestScript(decu.Script):
    """Script subclass used for testing purposes."""
    def __init__(self, tmpdir):
        self.logs_dir = tmpdir.mkdir('logs').dirname
        self.figures_dir = tmpdir.mkdir('pics').dirname
        super().__init__(datetime.datetime.now(), os.getcwd(), __name__)