# decu

![RTD Badge](https://readthedocs.org/projects/decu/badge/)

`decu` stands for "Decu is a Experimental Computation Utility". `decu`
arose from the need for standardization and automation of several
day-to-day tasks when running scripts for experimental computation. If
you've ever caught yourself spending more time in bookkeeping your files
and directories, or on committing small tweaks to your scripts, `decu` is
for you.


## Experimental Computation

We define a 'experimental computation' script as a script that reads some
data, performs an experiment (run an algorithm, train a model, plot a
figure, etc), saves some results to disk, and then quits. Some tasks that
are usually involved in this are:

1. file I/O: choosing file names for results and plots
2. multiprocessing: running many experiments/scripts in parallel
3. timekeeping: how long algorithms take to run
4. cloud service integration
5. logging

`decu` was born from the realization that none of these tasks have anything
to do with (and in fact get in the way of) the actual experimentation being
done. Furthermore, experimental computation scripts tend to mix together
code dedicated to these tasks with code intended to run the actual
algorithms of interest, thus making said algorithms harder to maintain and
debug.

The main goal of `decu` is to provide standardization and automation of
these tasks, with end code that clearly separate experimental computation
from bookkeeping and other auxiliary code.


## Installation

Clone this repo, `cd` to the decu directory and do

```
$ pip install .
```

Now you have a local installation of `decu`. If you are going to make edits
to `decu`, don't forget to use the `-e` flag.


## Usage

For a simple example, please see the
[quick start page](https://decu.readthedocs.io/en/latest/quickstart.html). For
more, see the
[tutorial](https://decu.readthedocs.io/en/latest/tutorial.html).

## Best practices

`decu` is built with Best Practices for Data Science in mind. For more, see

Wilson, Greg, et al. **Good Enough Practices in Scientific Computing.**
PLOS Computational Biology, vol. 13, no. 6, 2017,
doi:10.1371/journal.pcbi.1005510.

Wilson, Greg, et al. **Best Practices for Scientific Computing.** PLoS
Biology, vol. 12, no. 1, July 2014, doi:10.1371/journal.pbio.1001745.
