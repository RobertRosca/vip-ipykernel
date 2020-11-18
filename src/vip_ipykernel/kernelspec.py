"""Taken and modified from
https://github.com/ipython/ipykernel/blob/master/ipykernel/kernelspec.py
"""

import ipykernel.kernelspec

from ipykernel.kernelspec import (
    KERNEL_NAME,
    RESOURCES,
    make_ipkernel_cmd,
    get_kernel_dict,
    InstallIPythonKernelSpecApp,
    install,
)

import sys

def make_vip_ipkernel_cmd(mod='ipykernel_launcher', executable=None, extra_arguments=None, **kw):
    """Build Popen command list for launching an ViP-IPython kernel.

    Parameters
    ----------
    mod : str, optional (default 'ipykernel_launcher')
        A string of an IPython module whose __main__ starts an IPython kernel

    executable : str, optional (default sys.executable)
        The Python executable to use for the kernel process.

    extra_arguments : list, optional
        A list of extra arguments to pass when executing the launch code.

    Returns
    -------

    A Popen command list
    """

    # Copyright (c) IPython Development Team.
    # Distributed under the terms of the Modified BSD License.

    if executable is None:
        executable = sys.executable
    extra_arguments = extra_arguments or []
    #  When installing the ViP IPykernel, the first `-m` module call points to
    #  our `vip_ipykernel_launcher`, and the second module call points to the
    #  desired ipykernel launcher module
    arguments = [executable, '-m', 'vip_ipykernel.vip_ipykernel_launcher', '-m', mod, '-f', '{connection_file}']
    arguments.extend(extra_arguments)

    return arguments

ipykernel.kernelspec.make_ipkernel_cmd = make_vip_ipkernel_cmd

if __name__ == '__main__':
    InstallIPythonKernelSpecApp.launch_instance()
