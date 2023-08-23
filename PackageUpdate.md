# SENTIO® Prober Control - Python Bindings

## Instructions for package maintainer (updating the package) 

*This section is for the package maintainers at MPI Corporation. The following instructions are for creating a new release of the package. If you only want to use the package you do not need to do this! Just follow the instructions listed above for installing an existing package.*

### 1.) Update the Version number

Before creatinga new package update the version number in [this file](https://github.com/SentioProberDev/SentioProberControl/blob/master/pyproject.toml).

### 2.) Create a new release on GitHub with the new binary archive

When you create a new release the packages at PyPi.org will automatically be updated. You do not have to add any binaries to the release at github because the binaries can now be download from pypi.org (https://pypi.org/manage/project/sentio-prober-control/release/23.1.2/).

### 3.) Manually creating a package for distribution (optional)

There is no need to do this unless you want to distribute a package to a specific customer for testing. Otherwise just create a new release and 
distribute it to pip. However if you really want to manually create the package here is what you need to do:

```python -m build```

This command will create the dist folder and two package files.

```
dist/
  sentio-prober-control-23.1.2-py3-none-any.whl
  sentio-prober-control-23.1.2.tar.gz
```
