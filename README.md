# decu

`decu` stands for "Decu is a Experimental Computation Utility". `decu`
arose from the need for standardization and automation of several
day-to-day tasks when running scripts for experimental computation. If
you've ever caught yourself making silly mistakes or committing small
tweaks to your scripts, only to push them to some cloud repo and then
running them in the cloud, `decu` is for you.

We define a 'experimental computation' script as a script that reads some
data, performs an experiment (run an algorithm, train a model, plot a
figure, etc), saves some results to disk, and then quits. Some desired
features common to these tasks are:

1. Orderly, standardized logging
2. Standardized file names for results and plots
3. Devel and publish modes: during development, one usually doesn't need to
   run/test scripts with the same parameters as when publishing (e.g., plot
   all figure in 300 dpi but only in puslish mode)
4. Clearly separate result generation from plot construction
5. Multiprocessing / MapReduce
6. Configure libraries to work in a headless, cloud environment (for
   example, set the correct mpl backend when running headless)
7. Integrates well with cloud services: have an automatic startup script


# Best practices

`decu` is built with Best Practices for Data Science in mind. See
[1] http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745
[2] http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510
