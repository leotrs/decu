.. decu documentation master file, created by
   sphinx-quickstart on Fri Oct 20 10:47:56 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Overview
========

:code:`decu` stands for "Decu is a Experimental Computation
Utility". :code:`decu` arose from the need for standardization and
automation of several day-to-day tasks when running scripts for
experimental computation. If you've ever caught yourself making silly
mistakes or committing small tweaks to your scripts over and over again,
only to push them to some cloud repository and then running them in the
cloud, :code:`decu` is for you.

We define a 'experimental computation' script as a script that reads some
data, performs an experiment (run an algorithm, train a model, plot a
figure, etc), saves some results to disk, and then quits. :code:`decu`
tries to take the pain away from the menial bookkeeping tasks involved in
such a script such as logging, I/O, timekeeping, multiprocessing, and cloud
integration.

:code:`decu` was born from the realization that none of these tasks have
anything to do with (and in fact get in the way of) the actual
experimentation being done. Thus, :code:`decu` provides
standardization/automation of these tasks.

:code:`decu` is built with Best Practices for Data Science in mind. See `1
<http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745>`_
and `2
<http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510>`_.





.. toctree::
   :maxdepth: 2
   :caption: Documentation

   quickstart
   tutorial
   decu


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
