"""
main.py
-------

A library for experimental computation scripts.

"""

import os as _os
import logging as _logging
from functools import wraps as _wraps
from string import Template as _Template
from configparser import ConfigParser as _cp
config = _cp(interpolation=None)
config.read('/home/leo/code/decu/decu/config.ini')

__all__ = ['Script', 'config', 'experiment', 'figure', 'run_parallel']


class Script():
    """Base class for experimental computation scripts."""

    data_dir = config['Script']['data_dir']
    results_dir = config['Script']['results_dir']
    logs_dir = config['Script']['logs_dir']
    figures_dir = config['Script']['figures_dir']
    figure_fmt = config['Script']['figure_fmt']
    log_fmt = config['Script']['log_fmt']
    time_fmt = config['Script']['time_fmt']

    def __init__(self, start_time, working_dir, file_name):
        self.start_time = start_time
        self.working_dir = working_dir
        self.file_name = file_name
        self.module_name, _ = _os.path.splitext(file_name)

        logfile = '{}_{}.txt'.format(start_time, self.module_name)
        logfile = _os.path.join(working_dir, self.logs_dir, logfile)
        _logging.basicConfig(level=_logging.INFO, filename=logfile,
                            format=self.log_fmt, datefmt=self.time_fmt)
        self.logfile = logfile

    def make_result_file(self, exp_name, param):
        return _os.path.join(self.results_dir,
                            '{}_{}_{}.txt'.format(self.start_time,
                                                  exp_name, param))

    def make_figure_file(self, fig_name, suffix=None):
        if suffix is None:
            outfile = '{}_{}.{}'.format(self.start_time, fig_name,
                                        self.figure_fmt)
        else:
            outfile = '{}_{}_{}.{}'.format(self.start_time, fig_name,
                                           suffix, self.figure_fmt)
        return _os.path.join(self.figures_dir, outfile)


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
    from multiprocessing import Pool
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
        from inspect import getfullargspec
        index = getfullargspec(method).args.index(param_name)
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
        cfg = config['experiment']

        def exp_start_msg(param):
            temp = _Template(cfg['start_wo_param'] if exp_param is None
                             else cfg['start_w_param'])
            return temp.safe_substitute(exp_name=exp_name, param=param)

        def exp_end_msg(param, elapsed):
            temp = _Template(cfg['end_wo_param'] if exp_param is None
                             else cfg['end_w_param'])
            return temp.safe_substitute(exp_name=exp_name, param=param,
                                        elapsed=round(elapsed, 5))

        def write_results(result, outfile):
            """Write experiment results to disk."""
            import numpy as np
            np.savetxt(outfile, np.array(result))

        def wrote_results_msg(outfile, param):
            temp = _Template(cfg['wrote_wo_param'] if exp_param is None
                             else cfg['wrote_w_param'])
            return temp.safe_substitute(exp_name=exp_name, param=param,
                                        outfile=outfile)

        from time import time
        @_wraps(method)
        def decorated(*args, **kwargs):
            value = get_argument(method, exp_param, args, kwargs)
            _logging.info(exp_start_msg(value))

            start = time()
            result = method(*args, **kwargs)
            end = time()

            _logging.info(exp_end_msg(value, end - start))

            obj = args[0]
            outfile = obj.make_result_file(exp_name, value)
            write_results(result, outfile)
            _logging.info(wrote_results_msg(outfile, value))

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
            temp = _Template(config['figure']['wrote'])
            return temp.safe_substitute(fig_name=fig_name, outfile=outfile)

        import matplotlib.pyplot as plt
        @_wraps(method)
        def decorated(*args, suffix=None, **kwargs):
            method(*args, **kwargs)
            fig = plt.gcf()
            if save:
                obj = args[0]
                outfile = obj.make_figure_file(fig_name, suffix)
                fig.savefig(outfile)
                _logging.info(wrote_fig_msg(outfile))
            if show:
                plt.show()


        return decorated

    return _figure
