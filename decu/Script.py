"""
Script.py
---------

Main decu classes and decorators.

"""

import os
import logging
from functools import wraps
from string import Template
from datetime import datetime
from collections import defaultdict
from configparser import ConfigParser
from multiprocessing import Pool, Value, Lock
config = ConfigParser(interpolation=None)

print([os.path.join(os.path.dirname(__file__), 'decu.cfg'),
       os.path.expanduser('~/.decu.cfg'),
       os.path.join(os.getcwd(), 'decu.cfg')])

print(os.listdir(os.path.dirname(__file__)))
print(os.listdir(os.path.split(os.path.dirname(__file__))[0]))


config.read([os.path.join(os.path.dirname(__file__), 'decu.cfg'),
             os.path.expanduser('~/.decu.cfg'),
             os.path.join(os.getcwd(), 'decu.cfg')])

__all__ = ['Script', 'config', 'experiment', 'figure', 'run_parallel', 'read_result']

lock = Lock()
runs = defaultdict(lambda: Value('i', 0))

class Script():
    """Base class for experimental computation scripts."""

    data_dir = config['Script']['data_dir']
    results_dir = config['Script']['results_dir']
    logs_dir = config['Script']['logs_dir']
    figures_dir = config['Script']['figures_dir']
    scripts_dir = config['Script']['scripts_dir']
    gendata_dir = config['Script']['gendata_dir']
    figure_fmt = config['Script']['figure_fmt']
    log_fmt = config['Script']['log_fmt']
    time_fmt = config['Script']['time_fmt']

    def __init__(self, working_dir, file_name):
        self.start_time = datetime.now()
        self.working_dir = working_dir
        self.file_name = file_name
        self.module_name, _ = os.path.splitext(file_name)

        os.makedirs(self.logs_dir, exist_ok=True)
        logfile = Template(config['Script']['log_file']).safe_substitute(
            time=self.start_time, module_name=self.module_name)
        logfile = os.path.join(working_dir, self.logs_dir, logfile)
        logging.basicConfig(level=logging.INFO, filename=logfile,
                            format=self.log_fmt, datefmt=self.time_fmt)
        self.logfile = logfile

    def make_result_file(self, exp_name, run, ext='txt'):
        temp = Template(config['Script']['result_file'])
        return os.path.join(self.results_dir,
                            temp.safe_substitute(time=self.start_time,
                                                 module_name=self.module_name,
                                                 exp_name=exp_name, run=run, ext=ext))

    def make_figure_file(self, fig_name, suffix=None):
        temp = Template(config['Script']['figure_wo_suffix_file'] if suffix is None else
                        config['Script']['figure_w_suffix_file'])
        outfile = temp.safe_substitute(time=self.start_time,
                                       module_name=self.module_name,
                                       fig_name=fig_name, suffix=suffix,
                                       ext=self.figure_fmt)
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

    with Pool(initializer=init, initargs=(lock, runs), maxtasksperchild=100) as pool:
        results = pool.starmap(exp, params)
    return results


def get_parameters(method, param_name, args, kwargs):
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


def write_result(result, outfile):
    """Write result to disk.

    Chose writing method according to result's type.

    """
    import numpy
    import pandas
    _type = type(result)

    if _type == numpy.ndarray:
        numpy.savetxt(outfile, numpy.array(result))
    elif _type == pandas.DataFrame:
        result.to_csv(outfile)
    else:
        numpy.savetxt(outfile, numpy.array(result))


def read_result(infile):
    """Read result from disk.

    Chose reading method according to result's type.

    """
    import numpy
    import pandas

    _, ext = os.path.splitext(infile)
    ext = ext.strip('.')

    if ext == 'txt':
        data = numpy.loadtxt(infile)
    elif ext == 'csv':
        data = pandas.read_csv(infile)

    return data


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
            temp = Template(cfg['start_msg'])
            return temp.safe_substitute(exp_name=exp_name, run=run, params=params)

        def exp_end_msg(run, params, elapsed):
            temp = Template(cfg['end_msg'])
            return temp.safe_substitute(exp_name=exp_name, params=params,
                                        elapsed=round(elapsed, 5), run=run)

        def wrote_results_msg(run, outfile, params):
            temp = Template(cfg['write_msg'])
            return temp.safe_substitute(exp_name=exp_name, params=params,
                                        outfile=outfile, run=run)

        from time import time
        @wraps(method)
        def decorated(*args, **kwargs):
            obj = args[0]
            with lock:
                decorated.run = runs[decorated].value
                runs[decorated].value += 1

            # Make sure the output dir exists
            os.makedirs(obj.results_dir, exist_ok=True)

            values = get_parameters(method, data_param, args, kwargs)
            logging.info(exp_start_msg(decorated.run, values))

            start = time()
            result = method(*args, **kwargs)
            end = time()
            logging.info(exp_end_msg(decorated.run, values, end - start))
            outfile = obj.make_result_file(exp_name, decorated.run)
            write_result(result, outfile)
            logging.info(wrote_results_msg(decorated.run, outfile, values))

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
        fig_name = method.__name__

        def wrote_fig_msg(outfile):
            temp = Template(config['figure']['write'])
            return temp.safe_substitute(fig_name=fig_name, outfile=outfile)

        import matplotlib.pyplot as plt
        @wraps(method)
        def decorated(*args, suffix=None, **kwargs):
            obj = args[0]
            # Make sure the output dir exists
            os.makedirs(obj.figures_dir, exist_ok=True)

            method(*args, **kwargs)
            fig = plt.gcf()
            if save:
                outfile = obj.make_figure_file(fig_name, suffix)
                fig.savefig(outfile)
                logging.info(wrote_fig_msg(outfile))
            if show:
                plt.show()


        return decorated

    return _figure
