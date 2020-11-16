# ViP IPykernel

Venv in Parent IPykernel

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

Once the package is installed, run `python3 -m vip_ipykernel.kernelspec  --user`
to install the kernel, now when you run a notebook with the default `python3`
kernel it will instead use the venv in a parent directory.

## Acknowledgements

The kernel implementation and tests are largely copy-and-paste'd directly from
the [ipykernel project](https://github.com/ipython/ipykernel) with some minor
modifications made to search for a venv and launch python out of it if possilbe.

## Todo

- [ ] Integration into Jupyter Notebook/Lab logger
- [ ] Look at ways to show kernel errors
- [ ] Support for other environments:
  - [ ] Poetry-created venvs (`poetry env info --path`)
  - [ ] Pipenv-created venvs
  - [ ] Pyenv-created venvs
  - [ ] Conda-created environments
  - [ ] User-configured venvs
  - [ ] Reading from vscode configuration?
  - [ ] etc...
