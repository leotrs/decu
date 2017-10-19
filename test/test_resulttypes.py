"""
test_resulttypes.py
-------------------

Test reading and writing of different (result) file types.

"""

import util
import numpy as np
from os import listdir
from os.path import basename
from decu import experiment, read_result


def test_array(tmpdir):
    """Test reading and writing and array."""
    class TestArray(util.TestScript):
        @experiment(exp_param='size')
        def exp(self, size):
            return np.arange(size)

    script = TestArray(tmpdir)
    size = 10
    result_path = script.make_result_file('exp', size)
    result_filename = basename(result_path)

    assert result_filename not in listdir(script.results_dir)
    result = script.exp(size)
    assert result_filename in listdir(script.results_dir)

    assert isinstance(result, np.ndarray)
    loaded = read_result(result_path)
    assert isinstance(loaded, np.ndarray)
    assert (loaded == result).all()
