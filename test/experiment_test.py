"""
experiment_test.py
------------------

Test the @experiment decorator.

"""

import os
import util
import numpy as np
from decu import experiment
import matplotlib.pyplot as plt


def test_write(tmpdir):
    """Test that @experiment-decorated methods write their results to disk."""
    class TestWrite(util.TestScript):
        @experiment(data_param='data')
        def exp(self, data, param):
            return np.power(data, param)

    script = TestWrite(tmpdir)
    pval = 4
    result_filename = os.path.basename(
        script.make_result_file('exp', 0, pval))

    assert result_filename not in os.listdir(script.results_dir)
    script.exp(range(100), pval)
    assert result_filename in os.listdir(script.results_dir)
