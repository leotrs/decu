.. decu documentation master file, created by
   sphinx-quickstart on Fri Oct 20 10:47:56 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Overview
========

:code:`decu` stands for "Decu is a Experimental Computation
Utility". :code:`decu` is a suite of command line tools to automate the
menial tasks involved in the development of experimental computation
projects.

We define a "experimental computation" script as a script that reads some
data, performs an experiment (run an algorithm, train a model, plot a
figure, etc), saves some results to disk, and then quits. Some tasks that
are usually involved in this are:

1. file I/O: choosing file names for results and plots
2. multiprocessing: running many experiments/scripts in parallel
3. timekeeping: how long algorithms take to run
4. cloud service integration
5. logging

:code:`decu` was born from the realization that none of these tasks have
anything to do with (and in fact get in the way of) the actual
experimentation being done. Furthermore, experimental computation scripts
tend to mix together code dedicated to these tasks with code intended to
run the actual algorithms of interest, thus making said algorithms harder
to maintain and debug.

The main goal of :code:`decu` is to provide standardization and automation
of these tasks, with end code that clearly separates experimental
computation from bookkeeping and other auxiliary code.

:code:`decu` is built with Best Practices for Data Science, by Greg Wilson
et al, in mind. See `1
<http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745>`_
and `2
<http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510>`_.



.. toctree::
   :maxdepth: 2
   :caption: Documentation

   quickstart
   tutorial
   decu
