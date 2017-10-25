"""
io_test.py
----------

Tests for the decu.io module.

"""

import os
from numpy.random import random, randint
from decu.io import write_result, read_result, make_fullname


def helper(obj, name, tmpdir, comp=None):
    if comp is None:
        comp = lambda a, b: a == b
    basename = tmpdir.join(name)
    fullname = make_fullname(basename, type(obj))
    assert fullname not in tmpdir.listdir()
    write_result(obj, basename)
    assert fullname in tmpdir.listdir()
    read = read_result(fullname)
    assert comp(read, obj)
    os.remove(fullname)


def test_array(tmpdir):
    """numpy arrays should be handled correctly."""
    import numpy as np
    size = randint(10, 100)
    test = lambda o: helper(o, 'array', tmpdir, lambda a, b: (a == b).all())
    test(np.zeros(size))
    test(np.zeros((size, size * 2)))
    test(random(size=(size, size * 2)))


def test_graph(tmpdir):
    """nx.Graph should be handled correctly."""
    import networkx as nx
    test = lambda o: helper(o, 'graph', tmpdir, lambda a, b:
                            sorted(a.nodes()) == sorted(b.nodes()) and \
                            nx.isomorphism.is_isomorphic(a, b))
    graph = nx.florentine_families_graph()
    test(graph)
