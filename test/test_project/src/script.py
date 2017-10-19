"""
testscript.py
-------------

This is a test script for decu.

"""

from decu import Script, experiment, figure, run_parallel
import logging
import numpy as np
import matplotlib.pyplot as plt


class TestScript(Script):

    @experiment(exp_param='param')
    def exp(self, data, param):
        """Compute x**param for each data point."""
        logging.info('Working hard for {}..'.format(param))
        return np.power(data, param)

    @figure()
    def plot_result(self, data, result):
        """Plot results of experiment."""
        plt.plot(data, result)

    @figure()
    def plot_many_results(self, data, results):
        """Plot results of experiment."""
        plt.figure()
        for param in results.keys():
            plt.plot(data, results[param])

    def main(self):
        """Run some experiments and make some figures."""
        data = np.arange(5)
        result1 = self.exp(data, param=4)
        self.plot_result(data, result1)

        param_list = np.arange(5, 10)
        result2 = run_parallel(self.exp, data, param_list)
        self.plot_many_results(data, result2, suffix='parallel')
