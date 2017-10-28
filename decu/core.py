"""
core.py
-------

Main decu classes and decorators.

"""

import os
import logging
from .config import config
from .logging import DecuLogger
from .io import write
from functools import wraps
from datetime import datetime
from collections import defaultdict
from multiprocessing import Pool, Value, Lock
if 'DISPLAY' not in os.environ:
    import matplotlib
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

__all__ = ['Script', 'experiment', 'figure', 'run_parallel', 'DecuException']


lock = Lock()
runs = defaultdict(lambda: Value('i', 0))


class DecuException(Exception):
    pass


class Script():
    """Base class for experimental computation scripts."""

    data_dir = config['Script']['data_dir']
    results_dir = config['Script']['results_dir']
    figures_dir = config['Script']['figures_dir']
    scripts_dir = config['Script']['scripts_dir']
    gendata_dir = config['Script']['gendata_dir']
    figure_fmt = config['Script']['figure_fmt']

    def __init__(self, project_dir="", module=None):
        self.start_time = datetime.now()
        self.project_dir = os.getcwd() if project_dir is None else project_dir
        self.module = self.__module__ if module is None else module
        self.log = DecuLogger(self.start_time, project_dir, self.module)

    def make_result_basename(self, exp_name, run):
        return os.path.join(self.results_dir, config['Script'].subs(
            'result_file', time=self.start_time, module_name=self.module,
            exp_name=exp_name, run=run))

    def make_figure_basename(self, fig_name, suffix=None):
        opt = 'figure_wo_suffix_file' if suffix is None \
              else 'figure_w_suffix_file'
        outfile = config['Script'].subs(
            opt, time=self.start_time, module_name=self.module,
            fig_name=fig_name, suffix=suffix, ext=self.figure_fmt)
        return os.path.join(self.figures_dir, outfile)


def run_parallel(exp, params):
    """Run an experiment in parallel.

    For each element `p` in `params`, call `exp(*p)`. These calls are made
    in parallel using multiprocessing.

    Args:
        exp (method): A @experiment-decorated method.
        params (list): Each element is a set of arguments to call `exp` with.

    Returns:
        dict: A dictionary where the key `pi` is an element of `params` and
        the value is the result of calling `exp(*pi)`.

    """
    def init(*args):
        global lock, runs
        lock, runs = args

    with Pool(initializer=init, initargs=(lock, runs),
              maxtasksperchild=100) as pool:
        results = pool.starmap(exp, params)
    return results


def _get_parameters(method, param_name, args, kwargs):
    """Return the arguments passed to all experimental parameters.

    All method arguments that are not param_name are treated as
    experimental parameter is method is assumed to have been called as
    method(*args, **kwargs).

    """
    from inspect import getfullargspec
    arg_values = kwargs.copy()
    arg_values.update(dict(zip(getfullargspec(method).args, args)))
    if param_name in arg_values:
        del arg_values[param_name]
    if 'self' in arg_values:
        del arg_values['self']
    return arg_values


def experiment(data_param=None):
    """Decorator that adds logging functionality to experiment methods.

    Args:

        data_param (str): Parameter treated by the method as data
        input. All other parameters are treated as experimental parameters.

    Returns:
        func: A decorator that adds bookkeeping functionality to its
        argument.

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
        cfg = config['experiment']

        def exp_start_msg(run, params):
            return cfg.subs('start_msg', exp_name=exp_name, run=run,
                            params=params)

        def exp_end_msg(run, params, elapsed):
            return cfg.subs('end_msg', exp_name=exp_name, params=params,
                            elapsed=round(elapsed, 5), run=run)

        def wrote_results_msg(run, outfile, params):
            return cfg.subs('write_msg', exp_name=exp_name, params=params,
                            outfile=outfile, run=run)

        from time import time

        @wraps(method)
        def decorated(self, *args, **kwargs):
            with lock:
                decorated.run = runs[decorated].value
                runs[decorated].value += 1

            # Make sure the output dir exists
            os.makedirs(self.results_dir, exist_ok=True)

            values = _get_parameters(method, data_param, args, kwargs)
            self.log.info(exp_start_msg(decorated.run, values))

            start = time()
            result = method(self, *args, **kwargs)
            end = time()
            self.log.info(exp_end_msg(decorated.run, values, end - start))
            basename = self.make_result_basename(exp_name, decorated.run)
            write(result, basename)
            self.log.info(wrote_results_msg(decorated.run, basename, values))

            return result

        return decorated

    return _experiment


def figure(show=False, save=True):
    """Create the figure decorator.

    Args:
        show (bool): Whether or not the figure should be shown.
        save (bool): Whether or not the figure should be saved to disk.

    Returns:
        func: A decorator that adds figure logging functionality to its
        argument.

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
        from inspect import getfullargspec
        fig_name = method.__name__
        spec = getfullargspec(method)
        if 'suffix' in spec.args or 'suffix' in spec.kwonlyargs:
            raise DecuException('methods decorated with decu.experiment '
                                'cannot have a \'suffix\' argument.')

        def wrote_fig_msg(outfile):
            return config['figure'].subs('write', fig_name=fig_name,
                                         outfile=outfile)

        @wraps(method)
        def decorated(self, *args, suffix=None, **kwargs):
            # Make sure the output dir exists
            os.makedirs(self.figures_dir, exist_ok=True)

            method(self, *args, **kwargs)
            fig = plt.gcf()
            if save:
                outfile = self.make_figure_basename(fig_name, suffix)
                fig.savefig(outfile)
                self.log.info(wrote_fig_msg(outfile))
            if show:
                plt.show()

        return decorated

    return _figure
