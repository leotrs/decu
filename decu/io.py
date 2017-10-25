"""
io.py
-----

Reading and writing functionality for decu.

"""

import os

__all__ = ['write_result', 'read_result']


def write_result(result, basename):
    """Write result to disk.

    Chose writing method according to result's type.

    """
    import numpy
    import pandas
    _type = type(result)

    if _type == numpy.ndarray:
        numpy.savetxt(basename, numpy.array(result))
    elif _type == pandas.DataFrame:
        result.to_csv(basename)
    else:
        numpy.savetxt(basename, numpy.array(result))


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
