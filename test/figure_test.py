"""
figure_test.py
--------------

Test the @figure decorator.

"""

import os
from decu import figure
import util
import matplotlib.pyplot as plt


def test_save_false(tmpdir):
    """Test the behavior of @figure when save=False."""
    class TestSaveFalse(util.TestScript):
        @figure(save=False)
        def plot(self):
            plt.figure()
            plt.plot(range(100), [x**2 for x in range(100)])

    script = TestSaveFalse(tmpdir)
    fig_filename = script.make_figure_file('plot')

    assert fig_filename not in tmpdir.listdir()
    script.plot()
    assert fig_filename not in tmpdir.listdir()


def test_save_true(tmpdir):
    """Test the behavior of @figure when save=True."""
    class TestSaveTrue(util.TestScript):
        @figure(save=True)
        def plot(self):
            plt.figure()
            plt.plot(range(100), [x**2 for x in range(100)])

    script = TestSaveTrue(tmpdir)
    fig_filename = script.make_figure_file('plot')

    assert fig_filename not in tmpdir.listdir()
    script.plot()
    assert fig_filename in tmpdir.listdir()


def test_suffix(tmpdir):
    """Test the suffix argument of @figure."""
    class TestSuffix(util.TestScript):
        @figure(save=True)
        def plot(self):
            plt.figure()
            plt.plot(range(100), [x**2 for x in range(100)])

    script = TestSuffix(tmpdir)
    suffix = 'test_suffix'
    fig_filename = script.make_figure_file('plot', suffix)

    assert fig_filename not in tmpdir.listdir()
    script.plot(suffix=suffix)
    assert fig_filename in tmpdir.listdir()
