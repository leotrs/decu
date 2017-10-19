"""
run_parallel_test.py
--------------------

Test the run_parallel function.

"""

from decu import run_parallel
import util

class MyTestScript(util.TestScript):
    def experiment(self, data, exponent):
        return data**exponent


def test_result_order(tmpdir):
    """Test that the result is returned in the correct order."""
    script = MyTestScript(tmpdir)
    data = 10
    params = range(10)
    results = run_parallel(script.experiment, data, params)

    assert results == {p: script.experiment(data, p) for p in params}
