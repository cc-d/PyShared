#!/usr/bin/env python3
import os
import os.path as op
from importlib import import_module

DIR = op.abspath(op.dirname(__file__))
PSDIR = op.abspath(op.join(DIR, 'pyshared'))
VF = op.join(PSDIR, "version.py")
PPF = op.join(DIR, "pyproject.toml")

vmod = import_module("pyshared.version")
cv = vmod.__version__

nv = input("Enter new version (current: {}): ".format(cv))


with open(VF, "w") as f:
    f.write(f"__version__ = '{nv}'\n")

with open(PPF, "r") as f:
    pyproj_lines = f.read().splitlines()
    for i in range(len(pyproj_lines)):
        if pyproj_lines[i].startswith("version ="):
            pyproj_lines[i] = f'version = "{nv}"'
            break


with open(PPF, "w") as f:
    f.write('\n'.join(pyproj_lines))

print("Version updated from {} to {}.".format(cv, nv))
