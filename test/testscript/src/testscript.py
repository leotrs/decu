"""
testscript.py
-------------

This is a test script for decu.

"""

from decu import *
import logging
import numpy as np
import matplotlib.pyplot as plt


@experiment(arg_param='param')
def exp(data, param):
    """Compute x**param for each data point."""
    logging.info('Working hard..')
    return np.array([np.power(x, param) for x in data])

# @figure
def plot_results(data, result):
    """Plot results of exp1."""
    plt.figure()
    for param in result.keys():
        plt.plot(data, result[param])
    plt.show()

def main():
    """Run exp1, exp2 and make the figures."""
    data = np.arange(5)
    param_list1 = np.arange(5)
    result1 = {p: exp(data, param=p) for p in param_list1}
    plot_results(data, result1)

    param_list2 = np.arange(5, 10)
    result2 = run_parallel(exp, data, param_list2)
    plot_results(data, result2)
