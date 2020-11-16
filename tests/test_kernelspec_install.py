"""Taken and modified from

https://github.com/ipython/ipykernel/blob/master/ipykernel/tests/test_kernelspec.py
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import io
import json
import os
from unittest import mock

import nose.tools as nt
import pytest
from jupyter_core.paths import jupyter_data_dir

from vip_ipykernel.kernelspec import (
    KERNEL_NAME,
    RESOURCES,
    InstallViPIPythonKernelSpecApp,
    install,
)


def assert_is_spec(path):
    for fname in os.listdir(RESOURCES):
        dst = os.path.join(path, fname)
        assert os.path.exists(dst)
    kernel_json = os.path.join(path, "kernel.json")
    assert os.path.exists(kernel_json)
    with io.open(kernel_json, encoding="utf8") as f:
        json.load(f)


def test_install_kernelspec(tmp_path):
    InstallViPIPythonKernelSpecApp.launch_instance(
        argv=["--prefix", str(tmp_path)]  # `launch_instance` does not like `Path`
    )

    assert_is_spec(os.path.join(tmp_path, "share", "jupyter", "kernels", KERNEL_NAME))


def test_install_user(tmp_path):
    with mock.patch.dict(os.environ, {"HOME": str(tmp_path)}):
        install(user=True)
        data_dir = jupyter_data_dir()

    assert_is_spec(os.path.join(data_dir, "kernels", KERNEL_NAME))


def test_install(tmp_path):
    with mock.patch("jupyter_client.kernelspec.SYSTEM_JUPYTER_PATH", [tmp_path]):
        install()

    assert_is_spec(os.path.join(tmp_path, "kernels", KERNEL_NAME))


def test_install_profile(tmp_path):
    with mock.patch("jupyter_client.kernelspec.SYSTEM_JUPYTER_PATH", [tmp_path]):
        install(profile="Test")

    spec = os.path.join(tmp_path, "kernels", KERNEL_NAME, "kernel.json")

    with open(spec) as f:
        spec = json.load(f)

    assert spec["display_name"].endswith(" [profile=Test]")

    nt.assert_equal(spec["argv"][-2:], ["--profile", "Test"])


def test_install_display_name_overrides_profile(tmp_path):
    with mock.patch("jupyter_client.kernelspec.SYSTEM_JUPYTER_PATH", [tmp_path]):
        install(display_name="Display", profile="Test")

    spec = os.path.join(tmp_path, "kernels", KERNEL_NAME, "kernel.json")

    with open(spec) as f:
        spec = json.load(f)

    assert spec["display_name"] == "Display"


@pytest.mark.parametrize("env", [None, dict(spam="spam"), dict(spam="spam", foo="bar")])
def test_install_env(tmp_path, env):
    # python 3.5 // tmp_path must be converted to str
    with mock.patch("jupyter_client.kernelspec.SYSTEM_JUPYTER_PATH", [str(tmp_path)]):
        install(env=env)

    spec = tmp_path / "kernels" / KERNEL_NAME / "kernel.json"
    with spec.open() as f:
        spec = json.load(f)

    if env:
        assert len(env) == len(spec["env"])
        for k, v in env.items():
            assert spec["env"][k] == v
    else:
        assert "env" not in spec
