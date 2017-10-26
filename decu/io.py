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
    nx.Graph: lambda fn, res: nx.write_gml(res, fn),
    int: lambda fn, res: _simple_write(fn, res, fmt=':d'),
    float: lambda fn, res: _simple_write(fn, res, fmt=':f')
})

read_funcs = {
    'txt': lambda fn: np.loadtxt(fn),
    'csv': lambda fn: pd.read_csv(fn, index_col=0),
    'gml': lambda fn: nx.read_gml(fn, destringizer=int),
    'int': lambda fn: _simple_read(fn, int),
    'float': lambda fn: _simple_read(fn, float),
    'json': lambda fn: _read_json(fn)
}

extensions = defaultdict(lambda: 'txt')
extensions.update({
    np.ndarray: 'txt',
    pd.DataFrame: 'csv',
    nx.Graph: 'gml',
    int: 'int',
    float: 'float',
    dict: 'json'
})


def make_fullname(basename, _type=None):
    """Return the basename plus an appropriate extension for the type."""
    return '{}.{}'.format(basename, extensions[_type])


def _simple_write(filename, obj, fmt=None):
    """Write str(obj) to a file. If fmt is given, format the string first."""
    string = str(obj) if fmt is None else ('{' + fmt + '}').format(obj)
    with open(filename, 'w+') as file:
        file.write(string)


def _read_json(filename):
    with open(filename) as file:
        return json.load(file)


def _simple_read(filename, converter):
    """Read a file written with _simple_write."""
    with open(filename) as file:
        return converter(file.read())


def write(result, basename):
    """Write result to disk."""
    filename = make_fullname(basename, type(result))
    write_funcs[type(result)](filename, result)


def read(infile):
    """Read result from disk."""
    _, ext = os.path.splitext(infile)
    ext = ext.strip('.')
    return read_funcs[ext](infile)
