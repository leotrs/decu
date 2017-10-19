"""
experiment_test.py
------------------

Test the @experiment decorator.

"""

import decu
import util
import numpy as np
import matplotlib.pyplot as plt


def test_write(tmpdir):
    """Test that @experiment-decorated methods write their results to disk."""
    class TestWrite(util.TestScript):
        @decu.experiment(exp_param='param')
        def exp(self, data, param):
            return np.power(data, param)

    script = TestWrite(tmpdir)
    pval = 4
    result_filename = script.make_result_file('exp', pval)

    assert result_filename not in tmpdir.listdir()
    script.exp(range(100), pval)
    assert result_filename in tmpdir.listdir()
