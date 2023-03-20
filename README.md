[![GitHub issues](https://img.shields.io/github/issues/SentioProberDev/SentioProberControl.svg?maxAge=360)](https://github.com/SentioProberDev/SentioProberControl/issues)
[![Version](https://img.shields.io/github/release/SentioProberDev/SentioProberControl.svg?maxAge=360)](https://github.com/SentioProberDev/SentioProberControl/releases/)
[![Github All Releases](https://img.shields.io/github/downloads/SentioProberDev/SentioProberControl/total.svg)](https://github.com/SentioProberDev/SentioProberControl/releases/)
# SENTIO® Prober Control - Python Bindings
This archive contains a package with python bindings to control a [MPI SENTIO® probe station](https://www.mpi-corporation.com/ast/engineering-probe-systems/mpi-sentio-software-suite/).

![AST_Back_2A fw_](https://user-images.githubusercontent.com/2202567/204108957-0c7a864a-a526-4d32-a1ca-51985a0b01c6.png)

## Instructions for installing the SENTIO® prober control Python package

The package for controlling MPI probe stations running the MPI SENTIO Software suite is now available via pythons package index. To install the
package simply type:

```python -m pip install sentio-prober-control```

## Example-Scripts

A set of example scripts for python is maintained in a seperate archive at GitHub. 

https://github.com/SentioProberDev/Examples-Python

## Troubleshooting

If you have problems getting the package to work. Check wether an old version of the sentio-prober-control is still installed. To do so type

```python -m pip list```

if an older version is listed uninstall it first by using the command. 

```python -m pip uninstall sentio-prober-control```

After the uninstallation you can proceed with the installation as explained in the section above.

## Instructions for package maintainer (updating the package) 

*This section is for the package maintainers at MPI Corporation. The following instructions are for creating a new release of the package. If you only want to use the package you do not need to do this! Just follow the instructions listed above for installing an existing package.*

This section explains how to manually build a package. You do not have to do this! Packages will be automatically build and pushed to
the python package index when a new release is drafted on GitHub!

1.) Update the Version information in [pyproject.toml](https://github.com/SentioProberDev/SentioProberControl/blob/master/pyproject.toml)

2.) Rebuild the package

```py -m build```

This command will create the dist folder and put the two package files into it.

```
dist/
  sentio-prober-control-23.1.2-py3-none-any.whl
  sentio-prober-control-23.1.2.tar.gz
```
