"""
figure_test.py
--------------

Test the @figure decorator.

"""

from os import listdir
from os.path import basename
from decu import figure, DecuException
import util
import matplotlib.pyplot as plt
import pytest


def test_save_false(tmpdir):
    """With save=False, @figure should not write to disk."""
    class TestSaveFalse(util.TestScript):
        @figure(save=False)
        def plot(self):
            plt.figure()
            plt.plot(range(100), [x**2 for x in range(100)])

    script = TestSaveFalse(tmpdir)
    fig_filename = basename(script.make_figure_basename('plot'))

    assert fig_filename not in listdir(script.figures_dir)
    script.plot()
    assert fig_filename not in listdir(script.figures_dir)


def test_save_true(tmpdir):
    """With save=True, @figure should write to disk."""
    class TestSaveTrue(util.TestScript):
        @figure(save=True)
        def plot(self):
            plt.figure()
            plt.plot(range(100), [x**2 for x in range(100)])

    script = TestSaveTrue(tmpdir)
    fig_filename = basename(script.make_figure_basename('plot'))

    assert fig_filename not in listdir(script.figures_dir)
    script.plot()
    assert fig_filename in listdir(script.figures_dir)


def test_suffix(tmpdir):
    """@figure-decorated methods should accept a suffix argument."""
    class TestSuffix(util.TestScript):
        @figure(save=True)
        def plot(self):
            plt.figure()
            plt.plot(range(100), [x**2 for x in range(100)])

    script = TestSuffix(tmpdir)
    suffix = 'test_suffix'
    fig_filename = basename(script.make_figure_basename('plot', suffix))

    assert fig_filename not in listdir(script.figures_dir)
    script.plot(suffix=suffix)
    assert fig_filename in listdir(script.figures_dir)


def test_suffix_override(tmpdir):
    """@figure-decorated methods cannot have a 'suffix' argument."""
    with pytest.raises(DecuException):
        class TestSuffixOverride(util.TestScript):
            @figure(save=True)
            def plot(self, suffix):
                plt.figure()
                plt.plot(range(100), [x**2 for x in range(100)])
