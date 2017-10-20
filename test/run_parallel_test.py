"""
run_parallel_test.py
--------------------

Test the run_parallel function.

"""

from decu import run_parallel
import util


# These classes are outside of the test functions because they need to be
# sent to Pool (through run_parallel). Pool only accepts top-level
# definitions. Pytest will ignore them as their name starts with 'My'.
class MyTestResultOrder(util.TestScript):
    def experiment(self, data, exponent):
        return data**exponent


def test_result_order(tmpdir):
    """Test that the result is returned in the correct order."""
    script = MyTestResultOrder(tmpdir)
    data = 10
    params = [(data, p) for p in range(10)]
    results = run_parallel(script.experiment, params)
    assert results == [script.experiment(*p) for p in params]


class MyTestMultipleParams(util.TestScript):
    def experiment(self, data, exponent, bias):
        return data**exponent + bias


def test_multiple_params(tmpdir):
    """Test run_parallel when the experiment has multiple parameters."""
    script = MyTestMultipleParams(tmpdir)
    data = 10
    params = [(data, p, b) for p, b in zip(range(10), range(10, 20))]
    results = run_parallel(script.experiment, params)
    assert results == [script.experiment(*p) for p in params]
