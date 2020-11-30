import os
import sys
from pathlib import Path

from vip_ipykernel import venv_search


def test_venv_search(tmp_path):
    os.chdir(tmp_path)

    venv_bin = tmp_path / '.venv' / 'bin'
    venv_bin.mkdir(parents=True)

    venv_executable = venv_bin / 'python3'
    venv_executable.touch()

    #  Use 'in' instead of '==' as venv_search may return python3.x instead of 3
    assert str(venv_executable) in str(venv_search())


def test_venv_search_missing(tmp_path):
    os.chdir(tmp_path)

    #  Use 'in' instead of '==' as venv_search may return python3.x instead of 3
    assert str(Path(sys.executable).resolve()) in str(venv_search())
