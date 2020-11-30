<center><h1>ViP IPykernel</h1></center>

<center>
  <a href="https://www.repostatus.org/#active" target="_blank">
      <img src="https://img.shields.io/badge/repo%20status-active-brightgreen?style=flat-square" alt="Lifecycle">
  </a>
  <a href="https://github.com/RobertRosca/vip-ipykernel/releases" target="_blank">
      <img src="https://img.shields.io/github/release-date/RobertRosca/vip-ipykernel?style=flat-square" alt="GitHub Release Date">
  </a>
  <a href="https://github.com/robertrosca/vip-ipykernel/releases/latest" target="_blank">
      <img src="https://img.shields.io/github/release/robertrosca/vip-ipykernel.svg?style=flat-square" alt="Release">
  </a>
  <a href="https://pypi.org/project/vip-ipykernel" target="_blank">
      <img src="https://img.shields.io/pypi/v/vip-ipykernel?style=flat-square" alt="PyPI">
  </a>
</center>

<center>
  <a href="https://github.com/RobertRosca/vip-ipykernel/actions?query=workflow%3ATests" target="_blank">
      <img src="https://img.shields.io/github/workflow/status/RobertRosca/vip-ipykernel/Tests/main?label=Tests&style=flat-square" alt="GitHub Workflow Status (main)">
  </a>
  <a href="https://codecov.io/gh/RobertRosca/vip-ipykernel" target="_blank">
      <img src="https://img.shields.io/codecov/c/github/RobertRosca/vip-ipykernel?style=flat-square" alt="Codecov">
  </a>
</center>

<center><h1>   </h1></center>

Venv in Parent IPykernel - an IPython kernel for Jupyter that runs out the closest venv


- [Overview](#overview)
- [How it Works](#how-it-works)
- [Caveats and Gotchas](#caveats-and-gotchas)
  - [VSCode Jupyter Notebook Integration](#vscode-jupyter-notebook-integration)
  - [Venv Names](#venv-names)
- [Acknowledgements](#acknowledgements)
- [Todo](#todo)

## Overview

Do you use `venv`'s for all of your environments? Do you run Jupyter out of a
system/user installed location or via JupyterHub? Are you bored of making a
kernel for every single venv? Then this is the package for you!

vip-ipykernel overwrites the default `python3` kernel and replaces it with one
which will traverse directories upwards until it finds a `.venv` directory, if
it finds one then it will start the kernel with python out of that directory, if
it does not find a venv then it will carry on with the default python3.

NOTE: Your venv **must have ipykernel installed in it**, as this 'kernel' just
searches for and launches ipykernel out of the local venv. If ipykernel is not
available inside the venv then it will fail to start.

This only needs to be installed once, you can do this with `pip install
vip-ipykernel --user` to install it into your local user environment.

Once the package is installed, run `python3 -m vip_ipykernel.kernelspec --user`
to install the kernel, now when you run a notebook with the default `python3`
kernel it will instead use the venv in a parent directory.

If you want to revert the changes, run `python3 -m ipykernel install --user`,
this will re-install the default `python3` kernel.

Alternatively, if you don't want to overwrite the default kernel, then you can
pass a name (`python3 -m vip_ipykernel.kernelspec --user --name venv-kernel`) to
so that the kernel appears separately in the list of kernels and the default
behaviour is not modified.

## How it Works

The standard python3 kernel is:

```
{
 "argv": [
  "/usr/bin/python3",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "Python 3",
 "language": "python"
}
```

This just says "Run using `python3` to run `ipykernel_launcher` with an argument
`-f {connection_file}`". When you install the vip ipykernel this is replace by:

```
{
 "argv": [
  "/usr/bin/python3",
  "-m",
  "vip_ipykernel_launcher",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "Python 3",
 "language": "python"
}
```

Which will instead run the `vip_ipykernel.vip_ipykernel_launcher` module,
passing it the arguments `-m ipykernel_launcher -f {connection_file}`. The
module runs a function `venv_search` which looks in the current directory, and
upwards to any parent directories, until it finds a `.venv` or `venv` directory
containing `bin/python3`.

If it finds a venv with python3 in it, it passes the arguments `-m
ipykernel_launcher -f {connection_file}` to that python executable, which starts
and connects the kernel from that venv to your current session, in the same way
that a kernel installed for that specific venv would.

If it does not find a venv, then it will default to the system python executable
and behave like the standard `python3` kernel.

## Caveats and Gotchas

### VSCode Jupyter Notebook Integration

VSCode manages kernels for its notebooks with its own system, so it will not use
the vip-ipykernel.

### Venv Names

Currently only venv's named `.venv` or `venv` are searched for, if your venv has
a different name it won't be found, and if you have multiple venv's available
then the first one (sorted alphanumerically, so `.venv` takes priority over
`venv`) will be used.

## Acknowledgements

The kernel implementation and tests are largely copy-and-paste'd directly from
the [ipykernel project](https://github.com/ipython/ipykernel) with some minor
modifications made to search for a venv and launch python out of it if possible.

## Todo

- [ ] Expand tests to different versions of ipykernel/jupyter_core
- [ ] Look at ways to show kernel errors
- [ ] Support for other environments:
  - [ ] Poetry-created venvs (`poetry env info --path`)
  - [ ] Pipenv-created venvs
  - [ ] Pyenv-created venvs
  - [ ] Conda-created environments
  - [ ] User-configured venvs
  - [ ] Reading from vscode configuration?
  - [ ] etc...
