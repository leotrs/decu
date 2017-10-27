"""
io.py
-----

Reading and writing functionality for decu.

"""

import os
import json

__all__ = ['write', 'read']

write_funcs = {
    int: lambda fn, res: _simple_write(fn, res, fmt=':d'),
    float: lambda fn, res: _simple_write(fn, res, fmt=':f'),
    str: lambda fn, res: _simple_write(fn, res),
    dict: lambda fn, res: _json_write(fn, res)
}

read_funcs = {
    'int': lambda fn: _simple_read(fn, int),
    'txt': lambda fn: _simple_read(fn, str),
    'json': lambda fn: _json_read(fn),
    'float': lambda fn: _simple_read(fn, float)
}

extensions = {
    int: 'int',
    float: 'float',
    str: 'txt',
    dict: 'json'
}


def make_fullname(basename, _type=None):
    """Return the basename plus an appropriate extension for the type."""
    return '{}.{}'.format(basename, extensions.get(_type, None))


def _simple_write(filename, obj, fmt=None):
    """Write str(obj) to a file. If fmt is given, format the string first."""
    string = str(obj) if fmt is None else ('{' + fmt + '}').format(obj)
    with open(filename, 'w+') as file:
        file.write(string)


def _simple_read(filename, converter):
    """Read a file written with _simple_write."""
    with open(filename) as file:
        return converter(file.read())


def _json_write(filename, res):
    """Write a dict as json."""
    with open(filename, 'w+') as file:
        return json.dump(res, file)


def _json_read(filename):
    """Read a json into a dict."""
    with open(filename) as file:
        return json.load(file)


def write(result, basename):
    """Write result to disk."""
    filename = make_fullname(basename, type(result))
    write_funcs[type(result)](filename, result)


def read(infile):
    """Read result from disk."""
    _, ext = os.path.splitext(infile)
    ext = ext.strip('.')
    return read_funcs[ext](infile)


try:
    import networkx as nx
    extensions[nx.Graph] = 'gml'
    write_funcs[nx.Graph] = lambda fn, res: nx.write_gml(res, fn)
    read_funcs['gml'] = lambda fn: nx.read_gml(fn, destringizer=int)

except ImportError:
    pass


try:
    import pandas as pd
    extensions[pd.DataFrame] = 'csv'
    extensions[pd.Series] = 'csv'
    write_funcs[pd.DataFrame] = lambda fn, res: res.to_csv(fn)
    write_funcs[pd.Series] = lambda fn, res: res.to_csv(fn)
    read_funcs['csv'] = lambda fn: _read_csv(fn)

    def _read_csv(filename):
        """Read a csv and return a DataFrame or Series."""
        loaded = pd.read_csv(filename, index_col=0)
        if len(loaded.columns) == 1:
            return pd.read_csv(filename, index_col=0, header=None)[1]
        else:
            return loaded

except ImportError:
    pass


try:
    import numpy as np
    extensions[np.ndarray] = 'npy'
    write_funcs[np.ndarray] = lambda fn, res: np.save(fn, res)
    read_funcs['npy'] = lambda fn: np.load(fn)

except ImportError:
    pass
