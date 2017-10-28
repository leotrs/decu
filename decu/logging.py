"""
logging.py
----------

Logging system setup for decu, specially, make multiprocessing and logging
play nicely together.

"""

import os
import logging
from .config import config

__all__ = ['DecuLogger']

# logging.Handler objects cannot be pickled, and thus multiprocessing
# doesn't handle them well. In practice, this means that decu.Script
# objects cannot hold a reference to logging.Handler objects since they
# will be pickled when we call pool.map (from run_parallel). The solution
# is that decu.Script objects hold instead a DecuLogger object, that itself
# doesn't hold a reference to Handlers. The handlers (and indeed Loggers,
# Formatters, et al) all live inside the global loggers dictionary, where
# the keys are the logfiles. In this way we can safely pickle Scripts.
loggers = {}


class DecuLogger():

    def __init__(self, start_time, project_dir, module):
        self.logs_dir = config['logging']['logs_dir']
        self.log_fmt = config['logging']['log_fmt']
        self.time_fmt = config['logging']['time_fmt']

        logfile = os.path.join(
            project_dir, self.logs_dir, config['logging'].subs(
                'log_file', time=start_time, module_name=module))
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        self.logfile = logfile

        logger = logging.getLogger(logfile)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(logfile)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(self.log_fmt, datefmt=self.time_fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        loggers[logfile] = logger

    def log(self, level, msg):
        loggers[self.logfile].log(level, msg)

    def debug(self, msg):
        loggers[self.logfile].debug(msg)

    def info(self, msg):
        loggers[self.logfile].info(msg)

    def warning(self, msg):
        loggers[self.logfile].warning(msg)

    def error(self, msg):
        loggers[self.logfile].error(msg)

    def critical(self, msg):
        loggers[self.logfile].critical(msg)
