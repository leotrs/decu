"""
io.py
-----

Reading and writing functionality for decu.

"""

import os
import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict

__all__ = ['write', 'read']

write_funcs = defaultdict(lambda:
                          lambda fn, res: np.savetxt(fn, np.array(res)))
write_funcs.update({
    np.ndarray: lambda fn, res: np.savetxt(fn, res),
    pd.DataFrame: lambda fn, res: res.to_csv(fn),
    nx.Graph: lambda fn, res: nx.write_gml(res, fn)
})

read_funcs = {
    'txt': lambda fn: np.loadtxt(fn),
    'csv': lambda fn: pd.read_csv(fn, index_col=0),
    'gml': lambda fn: nx.read_gml(fn),
}

extensions = defaultdict(lambda: 'txt')
extensions.update({
    np.ndarray: 'txt',
    pd.DataFrame: 'csv',
    nx.Graph: 'gml'
})


def make_fullname(basename, _type=None):
    """Return the basename plus an appropriate extension for the type."""
    return '{}.{}'.format(basename, extensions[_type])


def write(result, basename):
    """Write result to disk."""
    filename = make_fullname(basename, type(result))
    write_funcs[type(result)](filename, result)


def read(infile):
    """Read result from disk."""
    _, ext = os.path.splitext(infile)
    ext = ext.strip('.')
    return read_funcs[ext](infile)
