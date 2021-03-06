"""
io_test.py
----------

Tests for the decu.io module.

"""

import os
from numpy.random import random, randint, choice
from decu.io import write, read, make_fullname
from pytest import importorskip


def helper(obj, name, tmpdir, comp=None):
    if comp is None:
        comp = lambda a, b: a == b
    basename = tmpdir.join(name)
    fullname = make_fullname(basename, type(obj))
    assert fullname not in tmpdir.listdir()
    write(obj, basename)
    assert fullname in tmpdir.listdir()
    loaded = read(fullname)
    assert comp(loaded, obj)
    os.remove(fullname)


def test_int(tmpdir):
    """ints should be handled correctly."""
    for _ in range(100):
        helper(randint(0, 10000), 'integer', tmpdir)


def test_float(tmpdir):
    """floats should be handled correctly."""
    for _ in range(100):
        helper(round(random(), 5), 'float', tmpdir)


def test_dict(tmpdir):
    for _ in range(100):
        helper({str(idx): round(random(), 5) for idx in range(100)},
               'dict', tmpdir)


def test_string(tmpdir):
    from string import ascii_uppercase
    for _ in range(100):
        helper(''.join(choice(list(ascii_uppercase), size=100)),
               'string', tmpdir)


def test_array(tmpdir):
    """numpy arrays should be handled correctly."""
    np = importorskip('numpy')
    size = randint(10, 100)
    test = lambda o: helper(o, 'array', tmpdir, lambda a, b: (a == b).all())
    test(np.zeros(size))
    test(np.zeros((size, size * 2)))
    test(random(size=(size, size * 2)))


def test_graph(tmpdir):
    """nx.Graph should be handled correctly."""
    nx = importorskip('networkx')
    test = lambda o: helper(o, 'graph', tmpdir, lambda a, b:
                            sorted(a.nodes()) == sorted(b.nodes()) and
                            nx.isomorphism.is_isomorphic(a, b))
    test(nx.florentine_families_graph())
    test(nx.karate_club_graph())
    test(nx.erdos_renyi_graph(100, 0.3))
    test(nx.barabasi_albert_graph(100, 3))
    test(nx.watts_strogatz_graph(100, 4, 0.2))


def test_series(tmpdir):
    """pd.Series should be handled correctly."""
    pd = importorskip('pandas')
    helper(pd.Series(random(size=100)), 'series', tmpdir,
           lambda a, b: round(sum(a-b), 10) == 0)


def test_dataframe(tmpdir):
    """pd.DataFrame should be handled correctly."""
    pd = importorskip('pandas')
    test = lambda o: helper(o, 'frame', tmpdir, lambda a, b:
                            len(a) == len(b) and
                            sorted(a.columns) == sorted(b.columns) and
                            len(pd.merge(a, b,
                                         on=list(a.columns),
                                         how='inner')) == len(a))
    size = 100
    test(pd.DataFrame({str(idx): randint(1, 10*size, size=size)
                       for idx in range(size)}))
