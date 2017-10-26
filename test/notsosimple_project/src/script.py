"""
testscript.py
-------------

This is a test script for decu.

"""

from decu import Script, experiment, figure, run_parallel
import numpy as np
import matplotlib.pyplot as plt


class TestScript(Script):

    @experiment(data_param='data')
    def exp(self, data, param, param2):
        """Compute x**param for each data point."""
        self.log.info('Working hard for {}..'.format(TestScript.exp.run))
        return np.power(data, param) + param2

    @figure()
    def plot_result(self, data, result):
        """Plot results of experiment."""
        plt.plot(data, result)

    @figure()
    def plot_many_results(self, data, results):
        """Plot results of experiment."""
        plt.figure()
        for res in results:
            plt.plot(data, res)

    def main(self):
        """Run some experiments and make some figures."""
        data = np.arange(5)
        result1 = self.exp(data, param=4, param2=10)
        self.plot_result(data, result1)

        param_list = [(data, x, y) for x, y in
                      zip(np.arange(5), np.arange(5, 10))]
        result2 = run_parallel(self.exp, param_list)
        self.plot_many_results(data, result2, suffix='parallel')
