"""
Script.py
-------

Main decu classes and decorators.

"""

import os
import logging
from functools import wraps
from string import Template
from datetime import datetime
from configparser import ConfigParser
config = ConfigParser(interpolation=None)
config.read([os.path.join(os.path.dirname(__file__), 'decu.cfg'),
             os.path.expanduser('~/.decu.cfg'),
             os.path.join(os.getcwd(), 'decu.cfg')])

__all__ = ['Script', 'config', 'experiment', 'figure', 'run_parallel', 'read_result']


class Script():
    """Base class for experimental computation scripts."""

    data_dir = config['Script']['data_dir']
    results_dir = config['Script']['results_dir']
    logs_dir = config['Script']['logs_dir']
    figures_dir = config['Script']['figures_dir']
    scripts_dir = config['Script']['scripts_dir']
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

    def make_result_file(self, exp_name, param, ext='txt'):
        temp = Template(config['Script']['result_file'])
        return os.path.join(self.results_dir,
                            temp.safe_substitute(time=self.start_time,
                                                 module_name=self.module_name,
                                                 exp_name=exp_name, param=param, ext=ext))

    def make_figure_file(self, fig_name, suffix=None):
        temp = Template(config['Script']['figure_file_wo_suffix'] if suffix is None else
                        config['Script']['figure_file_w_suffix'])
        outfile = temp.safe_substitute(time=self.start_time,
                                       module_name=self.module_name,
                                       fig_name=fig_name, suffix=suffix,
                                       ext=self.figure_fmt)
        return os.path.join(self.figures_dir, outfile)


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
            temp = Template(cfg['start_wo_param'] if exp_param is None
                             else cfg['start_w_param'])
            return temp.safe_substitute(exp_name=exp_name, param=param)

        def exp_end_msg(param, elapsed):
            temp = Template(cfg['end_wo_param'] if exp_param is None
                             else cfg['end_w_param'])
            return temp.safe_substitute(exp_name=exp_name, param=param,
                                        elapsed=round(elapsed, 5))

        def wrote_results_msg(outfile, param):
            temp = Template(cfg['wrote_wo_param'] if exp_param is None
                             else cfg['wrote_w_param'])
            return temp.safe_substitute(exp_name=exp_name, param=param,
                                        outfile=outfile)

        from time import time
        @wraps(method)
        def decorated(*args, **kwargs):
            obj = args[0]
            # Make sure the output dir exists
            os.makedirs(obj.results_dir, exist_ok=True)

            value = get_argument(method, exp_param, args, kwargs)
            logging.info(exp_start_msg(value))

            start = time()
            result = method(*args, **kwargs)
            end = time()
            logging.info(exp_end_msg(value, end - start))
            outfile = obj.make_result_file(exp_name, value)
            write_result(result, outfile)
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
            temp = Template(config['figure']['wrote'])
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
