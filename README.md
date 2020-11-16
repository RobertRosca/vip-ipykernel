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

This only needs to be installed once, you can do this with `pip install
vip-ipykernel --user` to install it into your local user environment,
alternatively I recommend using [pipx](https://github.com/pipxproject/pipx) to
install and run `vip-ipykernel` from an isolated environment.
