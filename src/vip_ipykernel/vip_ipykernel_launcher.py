"""Taken and modified from
https://github.com/ipython/ipykernel/blob/master/ipykernel_launcher.py

Entry point for launching an ViP-IPython kernel.
"""

import sys
from pathlib import Path
import subprocess
from traitlets import Instance
import logging

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

    Instance(logging.Logger)

    args[0] = str(venv_search())

    print(f"Starting venv kernel with args: {args}")

    subprocess.run(args)
