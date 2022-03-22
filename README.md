# pyTWTL - Python 3
## About
A Python 3 interface for code by Cristian Ioan Vasile <cvasile@bu.edu> from https://sites.bu.edu/hyness/twtl/ that translates a TWTL expression into a DFA. This is accomplished by packaging pyTWTL using PyInstaller and calling it from Python 3 via subprocess.

See the original readme, pyTWTL-readme.txt, for information on pyTWTL.

This package can be installed directly from GitHub:
```
pip install git+https://github.com/levivk/pyTWTL-python3@master
```
## Usage
```python
from pyTWTL.twtl_to_dfa import twtl_to_dfa

out = twtl_to_dfa("[H^1 r2]^[0,10]", kind="both")
alphabet = out['alphabet']      # The alphabet set
dfa_normal = out['normal']      # The normal dfa
dfa_relaxed = out['infinity']   # The relaxed dfa
```
