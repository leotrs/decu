# Quick Start

If you're in a hurry and want to enjoy all the benefits from `decu` without
having to go through a two hour long lecture, this is the place for you.

## Installation

Clone [this](https://github.com/leotrs/decu) repo, `cd` to the decu
directory and do

```
$ pip install .
```

Now you have a local installation of `decu`. If you are going to make edits
to `decu`, don't forget to use the `-e` flag.

## Start a new project

To start a new project, choose a directory in your file system, say
`root_dir`. Navigate to `root_dir` and execute the following command.

```
$ decu init
```

`decu` will generate the default directory structure under `root_dir`.

Here's the what you need to know in order to use `decu` inside `root_dir`:

+ All contents relating to your project (data, code, figures,
  documentation, manuscripts, etc) should be in subdirectories of
  `root_dir`.
+ All `decu` commands should be invoked from `root_dir`, not any of its
  subdirectories.

## Development

If you `ls` your `root_dir`, you will find a newly created `scr/`
directory. This is where all your computational experiments go. For this
example, we will use the following file, `script.py`:

```
import decu

class MyScript(decu.Script):
    @decu.experiment(data_param='data')
    def exp(self, data, param, param2):
        return [x**param + param2 for x in data]

    def main(self):
        data = range(100)
        result = self.exp(data, 2.72, 3.14)
```

Place this file inside `src/` and call the following command.

```
$ decu exec src/script.py
```

`decu` will run your script, leave a log file inside `logs/` and save the
results to disk inside `results/`.

Here's the what you need to know in order to develop `decu` scripts:

+ A script that is to be run with `decu` must subclass `decu.Script` and
  override the `main` function. Say you call this subclass `MyScript`.
+ Methods of `MyScript` that are intended to run your main algorithms
  should be decorated with `@decu.experiment`.
+ `decu.experiment`-decorated methods must accept at least one
  parameter. This will be treated as the data input, and its name must be
  passed to the decorator. In the above example, the `exp` method is
  decorated with `decu.experiment` with data input parameter *data*, and
  thus we pass the string `"data"` to `decu.experiment`.
+ All other parameters will be treated as experimental parameters that tune
  the behavior of the algorithm.

## Inspection

In the above example, we called `exp` with `param2 = 3.14`. Say we made a
mistake and the correct value for `param2` should have been `6.28`. Instead
of fixing the file and running the whole script again (which in a real
world scenario could be costly and/or time-consuming), with `decu` we have
an alternative.

After the last step, `decu` saved the results of your script in a file
inside `results/`. Call the file `<result_file1>`. Now execute:

```
$ decu inspect results/<result_file1>
>>> import decu
>>> import numpy as np
>>> import src.script as script
>>> script = script.MyScript('<root_dir>', 'script')
>>> # loaded result

In[1]:
```

What `decu` just did is initiate an iPython session ready for us to fix our
mistake. The contents of `<result_file1>` have been loaded in the variable
`result`.

Observe that we can fix our mistake by adding `3.14` to each element in the
`result` array. So we do so in iPython:

```
In[1]: result += 3.14
```

Our mistake is now fixed. We need only save the new result file, which we
can do manually with `numpy` (observe that `decu` loaded `numpy` for us
already):

```
In[2]: np.savetxt('results/fixed.txt', result)
```

Or, if we want to use the same naming scheme as `decu` is using for all
files, we can do the following. Note that `decu` also loaded in our iPython
session our `script.py` and instantiated `MyScript` as `script`:

```
In[3]: np.savetxt(script.make_result_file("exp", 0), result)
```

We need to specify `"exp"` as this was the `@decu.experiment`-decorated
method that originally created the result. We can close iPython now.

Here's what you need to know in order to use `decu inspect`:

+ `decu`'s default file names may seem complicated but they are useful when
  inspecting results, as `decu` can know from the file name what script,
  class, and method generated a result file.

## We're done!

In the course of this quick tour-de-force, we have a new directory
structure for our new project, added a script and fixed a minor mistake by
using `decu`'s inspecting capabilities. All bookkeeping, file names,
logging, and directories have been handled by `decu` for us.

This is only a sliver of what one can do with `decu`, but it should give
you the minimum you need to know to start using it in your projects.

For a more detailed example, see the [tutorial](tutorial.html).
