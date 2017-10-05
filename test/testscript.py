"""
testscript.py
-------------

This is a test script for decu.

"""

import decu
import numpy as np
import matplotlib.pyplot as plt


class MyScript(decu.Script):

    @experiment
    def exp1(self, data, param):
        """Compute x**param for each data point."""
        return [np.power(x**param) for x in data]

    @figure
    def plot_results1(self, result):
        # plot a figure from the results..
        plt.savefig(..)   # or plt.show()

    @experiment
    def exp2(self, data, param):
        """Compute x**1/param for each data point."""
        return [np.power(x, 1/param) for x in data]

    @figure
    def plot_results2(self, result):
        # plot results of experiment 2..
        plt.savefig(..)   # or plt.show()

    def main():
        data = np.arange(-10, 10, 0.1)
        param_list1 = np.arange(5)
        result1 = {p: self.exp1(data, param=p) for p in param_list1}
        print(result1)
        # self.plot_results1(result1)

        result2 = self.run_parallel(self.exp2, data, param_list2)
        print(result2)
        # self.plot_results2(result2)
