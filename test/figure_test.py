"""
figure_test.py
--------------

Test the @figure decorator.

"""

import os
import decu
import pytest
import datetime
import matplotlib.pyplot as plt


class MyTestScript(decu.Script):
    def __init__(self, tmpdir):
        self.LOGS_PATH = tmpdir.mkdir('logs').dirname
        self.FIGURES_PATH = tmpdir.mkdir('pics').dirname
        super().__init__(datetime.datetime.now(), os.getcwd(), __name__)


def test_figure_save_false(tmpdir):
    """Test the behavior of @figure when save=False."""
    class TestSaveFalse(MyTestScript):
        @decu.figure(save=False)
        def plot(self):
            plt.figure()
            plt.plot(range(100), [x**2 for x in range(100)])

    script = TestSaveFalse(tmpdir)
    fig_filename = script.make_figure_file('plot')

    assert fig_filename not in tmpdir.listdir()
    script.plot()
    assert fig_filename not in tmpdir.listdir()


def test_figure_save_true(tmpdir):
    """Test the behavior of @figure when save=True."""
    class TestSaveTrue(MyTestScript):
        @decu.figure(save=True)
        def plot(self):
            plt.figure()
            plt.plot(range(100), [x**2 for x in range(100)])

    script = TestSaveTrue(tmpdir)
    fig_filename = script.make_figure_file('plot')

    assert fig_filename not in tmpdir.listdir()
    script.plot()
    assert fig_filename in tmpdir.listdir()
