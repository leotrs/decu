# decu

![RTD Badge](https://readthedocs.org/projects/decu/badge/)

`decu` stands for "Decu is a Experimental Computation Utility". `decu`
arose from the need for standardization and automation of several
day-to-day tasks when running scripts for experimental computation. If
you've ever caught yourself making silly mistakes or committing small
tweaks to your scripts, only to push them to some cloud repo and then
running them in the cloud, `decu` is for you.


# Experimental Computation

We define a 'experimental computation' script as a script that reads some
data, performs an experiment (run an algorithm, train a model, plot a
figure, etc), saves some results to disk, and then quits. Some desired
features common to these tasks are:

1. Orderly, standardized logging
2. Standardized file names for results and plots (include datetime and
   script name in the results file name)
3. Devel and publish modes: during development, one usually doesn't need to
   run/test scripts with the same parameters as when publishing (e.g., plot
   all figure in 300 dpi but only in puslish mode)
4. Clearly separate result generation from plot construction
5. Multiprocessing / MapReduce
6. Configure libraries to work in a headless, cloud environment (for
   example, set the correct mpl backend when running headless)
7. Integrates well with cloud services: have an automatic startup script
8. Timekeeping of how long algorithms take to run

`decu` was born from the realization that none of these tasks have anything
to do with (and in fact get in the way of ) the actual experimentation
being done. Thus, `decu` provides standardization/automation of these
tasks.


# Installation

Clone this repo, `cd` to the decu directory and do

```
$ pip install .

```

Now you have a local installation of decu. If you are going to make edits
to decu, don't forget to use the `-e` flag.


# Example use

Suppose you have some data set and want to run an algorithm over it to
produce a figure for your latest research paper. Usually, the code would
involve
1. the algorithm itself,
2. reading data from disk (or other source),
3. calling the algorithm on the data set, perhaps in a loop that traverses the
  parameter space (or other method of model selection),
4. the plot to generate the figure,
5. write the results to disk, and maybe some clean up code

If you have some experience (and especially if you expect your script to
take a while to run), you might also include in your script

6. logging statements
7. multiprocessing, MapReduce or `asyncio`
8. measuring the time it takes your algorithm to run

The problem with the above is that only points 1 and 4 are directly related
to what the experimenter usually wants to do. The rest is usually
boilerplate, error-prone, and takes away time from the actual computational
experimentation one set out to do.

With `decu`, a script that does all of the above, will look like the
following,

```python
import decu

class MyScript(decu.Script):
    @experiment
    def exp1(self, data, param):
        # do something to the data... and get the result!
        return result

    @figure
    def plot_results1(self, result):
        # plot a figure from the results..
        plt.savefig(..)   # or plt.show()

    @experiment
    def exp2(self, data, param):
        # do magic to the data...
        return result

    @figure
    def plot_results2(self, result):
        # plot results of experiment 2..
        plt.savefig(..)   # or plt.show()

    def main():
        data = read_data()
        result1 = [self.exp_1(data, param=p) for p in param_list1]
        self.plot_results1(result1)

        result2 = self.run_parallel(self.exp_2, data, param_list2)
        self.plot_results2(result2)

```

Here, the user defines two different experiments and two different routines
to plot the results of said experiments. All the logging, multiprocessing,
reading, writing, and timekeeping have been handled by `decu`.

To run the above script, one can do

```
$ python decu my_script.py
```

which will call the `MyScript.main` function above. If the script is
particularly time-consuming, one can do

```
$ python decu my_script.py --cloud
```

which, after some setting up, will spin up a GCP instance and run the
script inside of it. Nifty, yes?


# Best practices

`decu` is built with Best Practices for Data Science in mind. See
[1] http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745
[2] http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510
