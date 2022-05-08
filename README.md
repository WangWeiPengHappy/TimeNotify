# TimeNotify
## Description
**Date**:2022-May-09

**Authur**:Eric

**Description**: 

A little python program to tell you the time to rest or do other things

## Build 

**My build tool**: py2app
- pip install py2app
- cd your_path/TimeNotify/
- py2applet --make-setup timer.py
- python setup.py py2app

**My python enviroment manager tools**

pyenv + virtualenv

***Note***

For support cpython(used by py2app), we should use the following way

```
env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.10.3
```
ref official link: [how-to-build-cpython-with-framework-support-on-os-x](https://github.com/pyenv/pyenv/wiki#how-to-build-cpython-with-framework-support-on-os-x)


## Others
To be update