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


    def __init__(self, mode='devel'):
        self.mode = mode

        try:
            filename = inspect.getfile(self.__class__)
        except TypeError as exc:
            # When defining a subclass on the interpretr, the subclass will
            # have no file attached.
            filename = '__main__'
        _, script_name = os.path.split(filename)
        path = os.getcwd()
        self.logfile = '{}_{}.txt'.format(NOW, script_name)
        self.logfile = os.path.join(path, self.LOGS_PATH, self.logfile)
        logging.basicConfig(level=logging.INFO, filename=self.logfile)

    def main(self, *args, **kwargs):
        """Override this method with the main contents of the script."""


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
        @functools.wraps(method)
        def msg(param):
            if arg_param is None:
                return 'Starting experiment {}..'.format(method.__name__)
            else:
                return 'Starting experiment {} with param {}..'.format(
                    method.__name__, param)

        def decorated(*args, **kwargs):
            logging.info(msg(kwargs.get(arg_param)))
            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()
            logging.info('Finished experiment. Took {}'.format(end - start))
            return result

        return decorated

    return _experiment
