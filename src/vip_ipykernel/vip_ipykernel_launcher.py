"""Taken and modified from
https://github.com/ipython/ipykernel/blob/master/ipykernel_launcher.py

Entry point for launching an ViP-IPython kernel.
"""

import logging
import subprocess
import sys
from pathlib import Path

from traitlets import Instance

VENV_NAMES = ['venv', '.venv']
ANCHOR = Path(Path.cwd().anchor)


def venv_search(prefix: Path = Path('.')) -> Path:
    prefix = prefix.absolute()

    found_venvs = []

    for venv in VENV_NAMES:
        found_venvs.extend(prefix.glob(f"{venv}/bin/python3"))

    if any(found_venvs):
        #  If there are multiple venvs just return the first one
        return found_venvs[0].absolute()
    elif prefix == ANCHOR:
        return Path(sys.executable)
    else:
        return venv_search(prefix=prefix.parent)


if __name__ == '__main__':
    # Remove the CWD from sys.path while we load stuff.
    # This is added back by InteractiveShellApp.init_path()
    if sys.path[0] == '':
        del sys.path[0]

    args = sys.argv

    args[0] = str(venv_search())

    #  TODO: I want to use the jupyter logger to print this off but can't figure
    #  out how to do that, @takluyver can you help with this?
    print(f"Starting venv kernel with args: {args}")

    subprocess.run(args)
