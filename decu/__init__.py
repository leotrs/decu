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
from datetime import datetime
from multiprocessing import Pool

NOW = datetime.now()


class Script():
    """Base class for experimental computation scripts.

    A script that is used for experimental computation usually performs the
    following tasts in order:

    1. Input: read data from disk, or scrape from the web,
    2. Experiment: run an algorithm, train a model, and/or produce a
    figure, and
    3. Output: write to disk a results file.

    Script provides basic standardization and automation for these tasks.

    """

    DATA_PATH = 'data/'
    RESULTS_PATH = 'results/'
    FIGURES_PATH = 'pics/'
    LOGS_PATH = 'logs/'
    LOG_FMT = '[%(asctime)s]%(levelname)s: %(message)s'
    TIME_FMT = '%H:%M:%S'

    def __init__(self, mode='devel'):
        self.mode = mode

        try:
            filename = inspect.getfile(self.__class__)
        except TypeError as exc:
            # When defining a subclass on the interpretr, the subclass will
            # have no file attached.
            filename = '__main__'
        _, script_name = os.path.split(filename)
        self.logfile = '{}_{}.txt'.format(NOW, script_name)
        self.logfile = os.path.join(os.getcwd(), self.LOGS_PATH, self.logfile)
        logging.basicConfig(level=logging.INFO, filename=self.logfile,
                            format=self.LOG_FMT, datefmt=self.TIME_FMT)

    def run_parallel(self, exp, data, params):
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


    def main(self, *args, **kwargs):
        """Override this method with the main contents of the script."""


def _get_arg_value(method, arg_name, args, kwargs):
    if arg_name in kwargs:
        return kwargs[arg_name]
    else:
        index = inspect.getfullargspec(method).args.index(arg_name)
        return args[index]


def experiment(arg_param=None):
    """Decorator that adds logging functionality to experiment methods.

    Parameters
    ----------

    arg_param (str): The name of the argument that is treated by the method
    as parameters of the experiment.

    Returns
    -------

    A decorator that adds logging and bookkeeping functionality to its
    argument.

    """
    def _experiment(method):
        exp_name = method.__name__

        def start_msg(param):
            if arg_param is None:
                return 'Starting experiment {}..'.format(exp_name)
            else:
                return 'Starting experiment {} with param {}..'.format(
                    exp_name, param)

        def end_msg(param, time):
            if arg_param is None:
                return 'Finished experiment {}..'.format(exp_name)
            else:
                return 'Finished experiment {} with param {}. Took {:.3f}s'.format(
                    exp_name, param, time)

        @functools.wraps(method)
        def decorated(*args, **kwargs):
            value = _get_arg_value(method, arg_param, args, kwargs)
            logging.info(start_msg(value))

            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()

            logging.info(end_msg(value, end - start))
            return result

        return decorated

    return _experiment
