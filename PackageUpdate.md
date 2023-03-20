# SENTIO® Prober Control - Python Bindings

## Instructions for package maintainer (updating the package) 

*This section is for the package maintainers at MPI Corporation. The following instructions are for creating a new release of the package. If you only want to use the package you do not need to do this! Just follow the instructions listed above for installing an existing package.*

0.) Update the Version number

Before creatinga new package update the version number in https://github.com/SentioProberDev/SentioProberControl/blob/master/pyproject.toml

1.) Create new package files:

```python -m build```

This command will create the dist folder.

```
dist/
  sentio-prober-control-3.8.0-py3-none-any.whl
  sentio-prober-control-3.8.0.tar.gz
```

4.) Create a new release on GitHub with the new binary archive

Make sure to manually add the created python package to the release.
