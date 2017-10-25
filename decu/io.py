"""
io.py
-----

Reading and writing functionality for decu.

"""

import os
import numpy as np
import pandas as pd
from collections import defaultdict

__all__ = ['write_result', 'read_result']

write_funcs = defaultdict(lambda:
                          lambda fn, res: np.savetxt(fn, np.array(res)))
write_funcs.update({
    np.ndarray: lambda fn, res: np.savetxt(fn, res),
    pd.DataFrame: lambda fn, res: res.to_csv(fn)
})

extensions = defaultdict(lambda: 'txt')
extensions.update({
    np.ndarray: 'txt',
    pd.DataFrame: 'csv'
})


def make_fullname(basename, _type=None):
    """Return the basename plus an appropriate extension for the type."""
    return '{}.{}'.format(basename, extensions[_type])


def write_result(result, basename):
    """Write result to disk.

    Chose writing method according to result's type.

    """
    filename = make_fullname(basename, type(result))
    write_funcs[type(result)](filename, result)


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
