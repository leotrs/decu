"""
test_resulttypes.py
-------------------

Test reading and writing of different (result) file types.

"""

import util
import numpy as np
from os import listdir
from os.path import basename, join
from decu import experiment, read_result
from decu.io import make_fullname


def test_array(tmpdir):
    """Test reading and writing and array."""
    class TestArray(util.TestScript):
        @experiment(data_param='size')
        def exp(self, size):
            return np.arange(size)

    script = TestArray(tmpdir)
    size = 10
    filename = make_fullname(basename(script.make_result_basename('exp', 0)))
    assert filename not in listdir(script.results_dir)
    result = script.exp(size)
    assert filename in listdir(script.results_dir)
    assert isinstance(result, np.ndarray)
    loaded = read_result(join(script.results_dir, filename))
    assert isinstance(loaded, np.ndarray)
    assert (loaded == result).all()
