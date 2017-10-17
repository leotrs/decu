"""
decu.py
-------

A library for experimental computation scripts.

"""

import os
import time
import logging
import inspect
import functools
import numpy as np
from multiprocessing import Pool
import matplotlib.pyplot as plt

__all__ = ['Script', 'experiment', 'run_parallel']


class Script():
    """Base class for experimental computation scripts."""

    data_path = 'data/'
    results_path = 'results/'
    figures_path = 'pics/'
    logs_path = 'logs/'
    log_fmt = '[%(asctime)s]%(levelname)s: %(message)s'
    time_fmt = '%H:%M:%S'


    def __init__(self, start_time, working_dir, file_name):
        self.start_time = start_time
        self.working_dir = working_dir
        self.file_name = file_name
        self.module_name, _ = os.path.splitext(file_name)

        logfile = '{}_{}.txt'.format(start_time, self.module_name)
        logfile = os.path.join(working_dir, self.logs_path, logfile)
        logging.basicConfig(level=logging.INFO, filename=logfile,
                            format=self.log_fmt, datefmt=self.time_fmt)
        self.logfile = logfile

    def make_result_file(self, exp_name, param):
        return os.path.join(self.results_path,
                            '{}_{}_{}.txt'.format(self.start_time,
                                                  exp_name, param))

    def make_figure_file(self, fig_name, suffix=None):
        if suffix is None:
            outfile = '{}_{}.png'.format(self.start_time, fig_name)
        else:
            outfile = '{}_{}_{}.png'.format(self.start_time, fig_name, suffix)
        return os.path.join(self.figures_path, outfile)


def run_parallel(exp, data, params):
    """Run an experiment in parallel.

    For each element p in params, call exp(data, p). These calls
    are made in parallel using multiprocessing.

    Parameters
    ----------

    exp (method): a method of this class that has been decoreted with
    @experiment.

    data (varies): the data set to feed the experiment.

    params (list): the experiment will be run once for each element in
    params.

    Returns
    -------

    A dictionary of the form {p1:  result1, p2: result2, ...} where the
    pi are the elements of params  and resulti is the result of calling
    exp(data, pi).

    """
    with Pool(maxtasksperchild=100) as pool:
        results = pool.starmap(exp, [(data, p) for p in params])
    return {p: results[i] for i, p in enumerate(params)}


def get_argument(method, param_name, args, kwargs):
    """Get the argument passed to the parameter with name param_name.

    method is assumed to have been called as method(*args, **kwargs).

    """
    if param_name in kwargs:
        return kwargs[param_name]
    else:
        index = inspect.getfullargspec(method).args.index(param_name)
        return args[index]


def experiment(exp_param=None):
    """Decorator that adds logging functionality to experiment methods.

    Parameters
    ----------

    exp_param (str): The name of the parameter that is treated by the
    method as a experimental parameter.

    Returns
    -------

    A decorator that adds bookkeeping functionality to its argument.

    """
    def _experiment(method):
        """Decorator that adds bookkeeping functionality to its argument.

        Parameters
        ----------

        method (function): A experimental computation function.

        Returns
        -------

        The method function, with added logging and bookkeeping
        functionality.

        """
        exp_name = method.__name__

        def exp_start_msg(param):
            if exp_param is None:
                return 'Starting experiment {}..'.format(exp_name)
            else:
                return 'Starting experiment {} with param {}..'.format(
                    exp_name, param)

        def exp_end_msg(param, elapsed):
            if exp_param is None:
                return 'Finished experiment {}..'.format(exp_name)
            else:
                return 'Finished experiment {} with param {}. Took {:.3f}s'.format(
                    exp_name, param, elapsed)

        def write_results(result, outfile):
            """Write experiment results to disk."""
            np.savetxt(outfile, np.array(result))

        def wrote_results_msg(outfile, param):
            if exp_param is None:
                return 'Wrote results of experiment {} in file {}.'.format(
                    exp_name, outfile)
            else:
                return 'Wrote results of experiment {} with param {} in file {}.'.format(
                    exp_name, param, outfile)

        @functools.wraps(method)
        def decorated(*args, **kwargs):
            value = get_argument(method, exp_param, args, kwargs)
            logging.info(exp_start_msg(value))

            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()

            logging.info(exp_end_msg(value, end - start))

            obj = args[0]
            outfile = obj.make_result_file(exp_name, value)
            write_results(result, outfile)
            logging.info(wrote_results_msg(outfile, value))

            return result

        return decorated

    return _experiment



def figure(show=False, save=True):
    """Create the figure decorator.

    Parameters
    ----------

    show (bool): Whether or not the figure should be shown.

    save (bool): Whether or not the figure should be saved to disk.

    Returns
    -------

    A decorator that adds figure logging functionality to its argument.

    """
    def _figure(method):
        """Decorator that adds logging functionality to figure methods.

        The method must return while the figure is still in memory, i.e.,
        neither plt.show or plt.savefig must be called. The resulting
        decorated method has a 'suffix' parameter that accepts a string
        that will be appended to the output file name. The 'suffix'
        parameter must be passed as a keyword argument.

        Parameters
        ----------

        show (bool): Whether or not the figure should be shown.

        save (bool): Whether or not the figure should be saved to disk.

        Returns
        -------

        The figure method, with added logging functionality, and a new
        'suffix' parameter.

        """
        fig_name = method.__name__

        def wrote_fig_msg(outfile):
            return 'Wrote figure {} to file {}.'.format(fig_name, outfile)

        @functools.wraps(method)
        def decorated(*args, suffix=None, **kwargs):
            method(*args, **kwargs)
            fig = plt.gcf()
            if save:
                obj = args[0]
                outfile = obj.make_figure_file(fig_name, suffix)
                fig.savefig(outfile)
                logging.info(wrote_fig_msg(outfile))
            if show:
                plt.show()


        return decorated

    return _figure
