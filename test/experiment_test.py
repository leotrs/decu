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
    result_filename = os.path.basename(script.make_result_basename('exp', 0))

    assert result_filename not in os.listdir(script.results_dir)
    script.exp(range(100), pval)
    assert result_filename in os.listdir(script.results_dir)


def test_multiple_params(tmpdir):
    """Test that @experiment-decorated methods support multiple parameters."""
    class TestWrite(util.TestScript):
        @experiment(data_param='data')
        def exp(self, data, param1, param2):
            return np.power(data, param1) + param2

    script = TestWrite(tmpdir)
    p1val = 4
    p2val = 10
    result_filename = os.path.basename(script.make_result_basename('exp', 0))

    assert result_filename not in os.listdir(script.results_dir)
    script.exp(range(100), p1val, p2val)
    assert result_filename in os.listdir(script.results_dir)
