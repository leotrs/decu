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
        # self.start_time = None
        # self.finish_time = None

    def main(*args, **kwargs):
        """Override this method with the main contents of the script."""





def main():
    """Execute the script passed as command line argument."""
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Experimental computation utilities.')
    parser.add_argument('file', help='the script to be run')
    args = parser.parse_args()

    print(args)



if __name__ == '__main__':
    main()
