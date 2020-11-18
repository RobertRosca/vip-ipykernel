import os
import pathlib
import subprocess
import shutil
from unittest import mock

import pytest

import jupyter_client.kernelspec

import json
import sys

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute().parent
NB_FILE_STD = pathlib.Path(__file__).parent.absolute() / 'notebook-std.ipynb'
NB_FILE_VIP = pathlib.Path(__file__).parent.absolute() / 'notebook-vip.ipynb'


def test_nb_vip_no_venv(tmp_path):
    from vip_ipykernel.kernelspec import install as install_vip
    import vip_ipykernel.kernelspec

    os.chdir(tmp_path)

    shutil.copy(NB_FILE_STD, ".")

    #  Install the custom kernel
    with mock.patch.dict(os.environ, {"HOME": str(tmp_path)}):
        defaults = list(vip_ipykernel.kernelspec.make_vip_ipkernel_cmd.__defaults__)
        defaults[1] = str(sys.executable)  # Set the python executable path to python used for pytest
        defaults = tuple(defaults)
        with mock.patch.object(vip_ipykernel.kernelspec.make_vip_ipkernel_cmd, "__defaults__", defaults):
            dest = install_vip(user=True)

        with open(str(dest) + "/kernel.json") as f:
            spec = json.load(f)

        #  The kernel should be installed in tmp_path
        assert str(tmp_path) in jupyter_client.kernelspec.find_kernel_specs()['python3']

        #  The kernel should be running with the same python that is running the tests
        assert sys.executable in spec["argv"][0]

        #  Should be using the vip_ipykernel module
        assert "vip_ipykernel" in spec["argv"][2]

        #  Test the ViP kernel falling back to base python
        pytest.main([
            "--verbose",
            "--nbval",
            "notebook-std.ipynb",
        ])


def test_nb_vip_venv(tmp_path):
    from vip_ipykernel.kernelspec import install as install_vip
    import vip_ipykernel.kernelspec

    os.chdir(tmp_path)

    shutil.copy(NB_FILE_VIP, ".")

    #  Create venv in the temporary directory
    subprocess.run([
        "python3",
        "-m",
        "venv",
        ".venv"
    ])

    #  Install ipykernel in it
    subprocess.run([
        ".venv/bin/python3",
        "-m",
        "pip",
        "install",
        "ipykernel",
        "jupyter_client",
    ])

    #  Install the custom kernel
    with mock.patch.dict(os.environ, {"HOME": str(tmp_path)}):
        defaults = list(vip_ipykernel.kernelspec.make_vip_ipkernel_cmd.__defaults__)
        defaults[1] = str(sys.executable)  # Set the python executable path to python used for pytest
        defaults = tuple(defaults)
        with mock.patch.object(vip_ipykernel.kernelspec.make_vip_ipkernel_cmd, "__defaults__", defaults):
            dest = install_vip(user=True)

        with open(str(dest) + "/kernel.json") as f:
            spec = json.load(f)

        #  The kernel should be installed in tmp_path
        assert str(tmp_path) in jupyter_client.kernelspec.find_kernel_specs()['python3']

        #  The kernel should be running with the same python that is running the tests
        assert sys.executable in spec["argv"][0]

        #  Test the ViP kernel notbook
        pytest.main([
            "--verbose",
            "--nbval",
            "notebook-vip.ipynb",
        ])
