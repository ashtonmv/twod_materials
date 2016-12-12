[![Build Status](https://travis-ci.org/ashtonmv/twod_materials.svg?branch=master)](https://travis-ci.org/ashtonmv/twod_materials)
[![Coverage](https://codecov.io/gh/ashtonmv/twod_materials/coverage.svg?branch=master)](https://codecov.io/gh/ashtonmv/twod_materials)

<img src="https://s3.amazonaws.com/mashton/twod_materials_logo.png" alt="Drawing" width="200"/>

About twod_materials
====================

The official documentation for `twod_materials`, which includes a pretty
comprehensive set of tutorials, can be found
[here](https://pythonhosted.org/twod_materials/).

The [wiki pages](https://github.com/ashtonmv/twod_materials/wiki) contain the
unofficial but still well-maintained documentation for `twod_materials`,
including the tutorials.

# Overview #

`twod_materials` is a library of functions that I've used in my research on
discovering and characterizing 2D materials. Some of them I have used thousands
of times, and others I have used less than five times. The functions in
`twod_materials` have been designed with user-friendliness as a priority,
which occasionally comes at the expense of flexibility. For example, some of the
post-processing functions will assume you have used a certain directory
structure when organizing your calculations. The goal here was not to be
restrictive, but to be streamlined.

# Installation and setup #

The latest stable release can be installed with ``pip``:
```bash
pip install numpy
pip install twod_materials
```

Alternatively, the very latest (no promises) version of `twod_materials` can be
installed by cloning this repository. Once you've cloned it
on your system, run `pip install numpy` and then
`pip install -r requirements.txt` to install its dependencies. You should then
add its location to your system's `$PYTHONPATH` so you can import its
functions from anywhere. There are a few ways to do this, including adding the
following line to your `~/.bashrc` file:
```
  export PYTHONPATH=$PYTHONPATH:/path/to/twod_materials  # obviously change this
```
Edit config.yaml with your system's settings, following the template:
```
  mp_api: your_materials_project_api_key
  normal_binary: path_to_normal_vasp_executable
  twod_binary: path_to_twod_vasp_executable
  potentials: path_to_your_vasp_potentials
  queue_system: slurm_or_pbs
```
and then copy or move it to your home directory (~).

# How the package is structured #

There are five mature modules in `twod_materials`: `stability`,
`electronic_structure`, `pourbaix`, `friction`, and `intercalation`.
The `magnetism` module is, for now, still in its infancy. The `utils` module
is basically just a library of helper functions used throughout the other
packages.

Each of these modules has two submodules: `startup` and `analysis`. For
most modules, `startup` contains functions that set up and submit VASP
calculations by interacting with your machine's queue system (PBS or SLURM). It
might be helpful to think of the `startup` submodules as pre-processing tools.
The `analysis` submodules, then, contain post-processing functions. These
post-processing functions can be grouped into two main categories: functions for
analyzing data and functions for plotting it. All plotting functions use
`matplotlib`.

Throughout the package, there are a few configuration files that for the most
part don't need to be changed (as opposed to config.yaml, which does):
potcar_symbols.yaml and the yaml files under the `pourbaix` module.

See the [tutorials](https://github.com/ashtonmv/twod_materials/wiki/Tutorial-1:-stability)
for sample usage of every function in `twod_materials`.
