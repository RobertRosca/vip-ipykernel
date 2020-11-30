import json
import os
import pathlib
import shutil
import subprocess
import sys
import venv
from unittest import mock

import jupyter_client.kernelspec
import pytest

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute().parent
NB_FILE_STD = pathlib.Path(__file__).parent.absolute() / 'notebook-std.ipynb'
NB_FILE_VIP = pathlib.Path(__file__).parent.absolute() / 'notebook-vip.ipynb'


def test_nb_vip_no_venv(tmp_path, monkeypatch):
    import vip_ipykernel.kernelspec
    from vip_ipykernel.kernelspec import install as install_vip

    monkeypatch.chdir(tmp_path)

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
        assert pytest.main([
            "--verbose",
            "--nbval",
            "notebook-std.ipynb",
        ]) == 0


def test_nb_vip_venv(tmp_path, monkeypatch):
    import vip_ipykernel.kernelspec
    from vip_ipykernel.kernelspec import install as install_vip

    monkeypatch.chdir(tmp_path)

    shutil.copy(NB_FILE_VIP, ".")

    #  Create venv in the temporary directory
    venv.create(".venv", with_pip=True)

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
        assert pytest.main([
            "--verbose",
            "--nbval",
            "notebook-vip.ipynb",
        ]) == 0
