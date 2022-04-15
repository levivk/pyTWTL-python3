# pyTWTL - Python 3
## About
A Python 3 interface for code by Cristian Ioan Vasile <cvasile@bu.edu> from https://sites.bu.edu/hyness/twtl/ that translates a TWTL expression into a DFA. This is accomplished by packaging pyTWTL using PyInstaller and calling it from Python 3 via subprocess.

See the original readme, pyTWTL-readme.txt, for information on pyTWTL.

This package can be installed directly from GitHub:
```bash
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

## How to build

If you want to use this on a different architecture or otherwise run into problems that requires rebundling the Python 2 code, below is how you do that.

### Ubuntu

This method runs a Ubuntu 18.04 docker container and runs pyinstaller there. No need to install Python 2.

```bash
# install git, and docker
sudo apt install git docker.io -y

# clone this repository
git clone https://github.com/levivk/pyTWTL-python3
cd pyTWTL-python3/pyinstaller_build

# run the build script
./build.sh

# run the test
./test.sh

# You should get a few hundred lines of yaml output and no errors
```

### MacOS

Tested on macOS Catalina Version 10.15.7 and Monterey Version 12.3

```bash
# install homebrew https://brew.sh/
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# install pyenv
brew install pyenv
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Now close your shell and reopen it

# install python 2.7 with dev libraries
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 2.7.18
pyenv global 2.7.18

# clone this repository
git clone https://github.com/levivk/pyTWTL-python3
cd pyTWTL-python3/pyinstaller_build

# install dependencies
pip install -r requirements.txt

# run the build script
bash build.sh

# run the test
bash test.sh

# You should get a few hundred lines of yaml output and no errors

# Uninstall python 2.7
pyenv global system
pyenv uninstall 2.7.18
```
