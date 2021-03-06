"""Taken and modified from
https://github.com/ipython/ipykernel/blob/9cc8ea7103b8bb5a124b6906870994753dcdaf64/ipykernel_launcher.py

Entry point for launching an ViP-IPython kernel.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import sys

if __name__ == '__main__':
    # Remove the CWD from sys.path while we load stuff.
    # This is added back by InteractiveShellApp.init_path()
    if sys.path[0] == '':
        del sys.path[0]

    from vip_ipykernel import venv_search

    args = sys.argv.copy()

    args[0] = str(venv_search())

    #  TODO: I want to use the jupyter logger to print this off but can't figure
    #  out how to do that, @takluyver can you help with this?
    print(f"Starting venv kernel with args: {args}")

    os.execv(args[0], args)
