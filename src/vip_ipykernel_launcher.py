"""Taken and modified from
https://github.com/ipython/ipykernel/blob/master/ipykernel_launcher.py

Entry point for launching an ViP-IPython kernel.
"""

import subprocess
import sys

from vip_ipykernel import venv_search

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
