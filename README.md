[![GitHub issues](https://img.shields.io/github/issues/SentioProberDev/SentioProberControl.svg?maxAge=360)](https://github.com/SentioProberDev/SentioProberControl/issues)
[![Version](https://img.shields.io/github/release/SentioProberDev/SentioProberControl.svg?maxAge=360)](https://github.com/SentioProberDev/SentioProberControl/releases/)
# SENTIO® Prober Control - Python Bindings
This archive contains a package with python bindings to control a [MPI SENTIO® probe station](https://www.mpi-corporation.com/ast/engineering-probe-systems/mpi-sentio-software-suite/).

![AST_Back_2A fw_](https://user-images.githubusercontent.com/2202567/204108957-0c7a864a-a526-4d32-a1ca-51985a0b01c6.png)

## Instructions for installing the SENTIO® prober control Python package

The package for controlling MPI probe stations running the MPI SENTIO Software suite is now available via [pythons package index](https://pypi.org/project/sentio-prober-control/). To install the
package simply type:

```python -m pip install sentio-prober-control```

If you already have a version of the package installed you can update the existing package with this command:

```python -m pip install sentio-prober-control --upgrade```

You no longer need to download the package by yourself, just use pip. If you cannot access the internet from your machine you can still download the archives from [the release section of this project](https://github.com/SentioProberDev/SentioProberControl/releases/).

## Example-Scripts

A set of example scripts for python is maintained in a separate archive at GitHub. 

https://github.com/SentioProberDev/Examples-Python

## Troubleshooting

Most problems arise from having multiple python environments on the local machine and installing the sentio-prober-control package into the wrong python environment. You can list all installed packages with the command:

```python -m pip list```

Make sure that the sentio-prober-control package in the latest version is in that list.

## Instructions for Package maintainer

[Manually Building a Package](https://github.com/SentioProberDev/SentioProberControl/blob/master/PackageUpdate.md)
