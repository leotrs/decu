"""
experiment_test.py
------------------

Test the @experiment decorator.

"""

from os import listdir
from os.path import basename
import util
import numpy as np
from decu import experiment, config
from decu.io import make_fullname


def test_write(tmpdir):
    """@experiment-decorated methods should write their results to disk."""
    class TestWrite(util.TestScript):
        @experiment(data_param='data')
        def exp(self, data, param):
            return np.power(data, param)

    script = TestWrite(tmpdir)
    pval = 4
    result_filename = basename(script.make_result_basename('exp', 0))
    fullname = make_fullname(result_filename, np.ndarray)

    assert fullname not in listdir(script.results_dir)
    script.exp(range(100), pval)
    assert fullname in listdir(script.results_dir)


def test_multiple_params(tmpdir):
    """@experiment-decorated methods should support multiple parameters."""
    class TestWrite(util.TestScript):
        @experiment(data_param='data')
        def exp(self, data, param1, param2):
            return np.power(data, param1) + param2

    script = TestWrite(tmpdir)
    p1val = 4
    p2val = 10
    filename = basename(make_fullname(script.make_result_basename('exp', 0),
                                      np.ndarray))

    assert filename not in listdir(script.results_dir)
    script.exp(range(100), p1val, p2val)
    assert filename in listdir(script.results_dir)


def test_no_data(tmpdir):
    """@experiment-decorated methods should support no data_param."""
    class TestNoData(util.TestScript):
        @experiment(data_param=None)
        def exp(self, data, param1, param2):
            return np.power(data, param1) + param2

    script = TestNoData(tmpdir)
    p1val = 4
    p2val = 10
    filename = basename(make_fullname(script.make_result_basename('exp', 0),
                                      np.ndarray))

    assert filename not in listdir(script.results_dir)
    script.exp(range(100), p1val, p2val)
    assert filename in listdir(script.results_dir)


def test_no_result(tmpdir):
    """@experiment-decorated methods should support no return value."""
    class TestNoResult(util.TestScript):
        @experiment(data_param=None)
        def exp(self):
            return None

    fmt = '%(levelname)s: %(message)s'
    config.set('logging', 'log_fmt', fmt)
    script = TestNoResult(tmpdir)
    script.exp()
    with open(script.log.logfile) as file:
        line = file.readlines()[-1].strip()
    msg = config['experiment'].subs('no_result_msg', exp_name='exp', run=0)
    assert line == '%(levelname)s: %(message)s' % \
        {'levelname': 'WARNING', 'message': msg}
