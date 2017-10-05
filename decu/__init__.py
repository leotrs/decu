"""
decu.py
-------

A library for experimental computation scripts.

"""

import logging
from datetime import datetime


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


    def __init__(self, mode='devel'):
        self.mode = mode

    def main(self, *args, **kwargs):
        """Override this method with the main contents of the script."""
