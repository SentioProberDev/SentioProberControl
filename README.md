[![GitHub issues](https://img.shields.io/github/issues/SentioProberDev/SentioProberControl.svg?maxAge=360)](https://github.com/SentioProberDev/SentioProberControl/issues)
[![Version](https://img.shields.io/github/release/SentioProberDev/SentioProberControl.svg?maxAge=360)](https://github.com/SentioProberDev/SentioProberControl/releases/)
# SENTIO® Prober Control - Python Bindings
This archive contains a package with python bindings to control a [MPI SENTIO® probe station](https://www.mpi-corporation.com/ast/engineering-probe-systems/mpi-sentio-software-suite/).

![AST_Back_2A fw_](https://user-images.githubusercontent.com/2202567/204108957-0c7a864a-a526-4d32-a1ca-51985a0b01c6.png)

## Instructions for installing the SENTIO® prober control Python package

The package for controlling MPI probe stations running the MPI SENTIO Software suite is now available via [pythons package index](https://pypi.org/project/sentio-prober-control/). To install the
package simply type:

```python -m pip install sentio-prober-control```

You no longer need to download the package by yourself, just use pip.

## Example-Scripts

A set of example scripts for python is maintained in a seperate archive at GitHub. 

https://github.com/SentioProberDev/Examples-Python

## Troubleshooting

If you have problems getting the package to work. Check wether an old version of the sentio-prober-control is still installed. To do so type

```python -m pip list```

if an older version is listed uninstall it first by using the command. 

```python -m pip uninstall sentio-prober-control```

After the uninstallation you can proceed with the installation as explained in the section above.

## Instructions for Package maintainer

[Manually Building a Package](PackageUpdate.md)
