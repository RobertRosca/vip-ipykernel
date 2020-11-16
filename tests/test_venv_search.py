import os
import shutil
from pathlib import Path

from vip_ipykernel.vip_ipykernel_launcher import venv_search


def test_venv_search(tmp_path):
    os.chdir(tmp_path)

    venv_bin = tmp_path / '.venv' / 'bin'
    venv_bin.mkdir(parents=True)

    venv_executable = venv_bin / 'python3'
    venv_executable.touch()

    assert venv_executable == venv_search()


def test_venv_search_missing(tmp_path):
    os.chdir(tmp_path)

    assert Path(shutil.which("python3")).resolve() == venv_search()
