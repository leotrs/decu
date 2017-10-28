# Customizing `decu`

No two projects are the same, and thus `decu` is built with customization
and extensibility in mind. For this purpose, `decu` relies heavily on a
configuration file accessible by the user through `decu.config`. See the
`decu.config` module for more information.


## The configuration file

The configuration file is a standard `.ini` file, usually called
`decu.cfg`, and read by the `configparser` standard library. It's broken
down into sections pertaining different aspects of the `decu`
system. `decu` provides defaults for all options so no customization is
necessary before using `decu`. However, if you want to customize the
system, all you need to do is create a `decu.cfg` file in your project's
root directory and override some options. Which options are available and
how to override them is documented in a later section.


## How the config file is read

There are three configuration files that `decu` is aware of. Suppose you
are working on a project located at `root_dir`. Then, `decu` reads three
different configuration files, in the following order:
1. Global: The default `decu.cfg` configuration file that comes with the `decu`
   installation. Modify this file only if you want your changes to be
   system-wide.
2. User-local: `~/.decu.cfg`. Modify this file if you want all your (the
   user's) projects to see the same changes.
3. Project-local: `root_dir/decu.cfg`. Modify a single project.

Files read later have precedence, so you can always override the global
options by supplying a `decu.cfg` under your `root_dir`.

Note: it is not recommended to change options during the development of a
project. It is best to customize `decu` before development has started and
to stick to one configuration file for the duration of a project. At the
moment of writing, it is unclear which options are safe to customize during
the course of a project. Thus it is HIGHLY DISCOURAGED to modify the global
configuration file as the changes will take place even in projects that are
already in development. It is best to use project-local configuration files
for each project.


## Configuration options

Each configuration option is documented in the global configuration file,
which we paste here.

```eval_rst
.. literalinclude:: _static/decu.cfg
   :language: ini
```
