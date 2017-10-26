"""
util.py
-------

Testing utilities.

"""

import os
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
        super().__init__(str(tmpdir))


# Finalization code. This should be decorated with pytest.fixture, with
# argument 'scope' set to 'module' in any and all modules that will use it.
# See https://goo.gl/N9KDf1
def make_teardown_fixture(root_dir):
    def teardown():
        """Guarantee a clean slate before and after all tests in a module."""
        def clean_up():
            """Delete all files except scripts."""
            dirs = [v.strip('/') for k, v in decu.config['Script'].items()
                    if k.endswith('_dir')]
            dirs.remove(decu.config['Script']['scripts_dir'].strip('/'))
            for dir_name in [d for d in dirs if d in os.listdir(root_dir)]:
                for file in os.listdir(os.path.join(root_dir, dir_name)):
                    os.remove(os.path.join(root_dir, dir_name, file))

        clean_up()
        os.chdir(root_dir)
        yield None
        os.chdir('..')
        clean_up()
    return teardown
