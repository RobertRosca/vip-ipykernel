__version__ = '0.1.0a1'

import sys
from pathlib import Path

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
        return Path(sys.executable).resolve()
    else:
        return venv_search(prefix=prefix.parent)
