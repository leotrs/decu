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
from multiprocessing import Pool


DATA_PATH = 'data/'
RESULTS_PATH = 'results/'
FIGURES_PATH = 'pics/'
LOGS_PATH = 'logs/'
LOG_FMT = '[%(asctime)s]%(levelname)s: %(message)s'
TIME_FMT = '%H:%M:%S'


__all__ = ['Script', 'experiment', 'run_parallel']


class Script():
    """Base class for experimental computation scripts."""

    def __init__(self, start_time, working_dir, file_name):
        self.start_time = start_time
        self.working_dir = working_dir
        self.file_name = file_name
        self.module_name, _ = os.path.splitext(file_name)

        logfile = '{}_{}.txt'.format(start_time, self.module_name)
        logfile = os.path.join(working_dir, LOGS_PATH, logfile)
        logging.basicConfig(level=logging.INFO, filename=logfile,
                            format=LOG_FMT, datefmt=TIME_FMT)
        self.logfile = logfile


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

        @functools.wraps(method)
        def decorated(*args, **kwargs):
            value = get_argument(method, exp_param, args, kwargs)
            logging.info(exp_start_msg(value))

            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()

            logging.info(exp_end_msg(value, end - start))
            return result

        return decorated

    return _experiment
