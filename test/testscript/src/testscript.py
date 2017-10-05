"""
testscript.py
-------------

This is a test script for decu.

"""

from decu import Script, experiment
import numpy as np
import matplotlib.pyplot as plt


class MyScript(Script):
    """Dummy test class."""

    @experiment
    def exp1(self, data, param):
        """Compute x**param for each data point."""
        return np.array([np.power(x, param) for x in data])

    def plot_results1(self, result):
        """Plot results of exp1."""
        plt.figure()
        for param in result.keys():
            plt.plot(*result[param])
        plt.show()

    def main(self):
        """Run exp1, exp2 and make the figures."""
        data = np.arange(5)
        param_list1 = np.arange(5)
        result1 = {p: (data, self.exp1(data, param=p)) for p in param_list1}
        self.plot_results1(result1)
