# SENTIO® Prober Control - Python Bindings

## Instructions for package maintainer (updating the package) 

*This section is for the package maintainers at MPI Corporation. The following instructions are for creating a new release of the package. If you only want to use the package you do not need to do this! Just follow the instructions listed above for installing an existing package.*

1.) Get the latest version of setuptools and wheel:

```python -m pip install --user --upgrade setuptools wheel```

2.) Update the package Version number

Open the file setup.py an change the "version" attribute to the most current version of SENTIO tested with the python package. The python package is backwards
compatible and will run with older SENTIO versions in general but it may contain new API bindings that are missing in the old versions.

3.) create the distribution archive:

cd into the archive (where setup.py) is located.

```python setup.py sdist bdist_wheel```

This command will create the dist folder.

```
dist/
  sentio-prober-control-3.8.0-py3-none-any.whl
  sentio-prober-control-3.8.0.tar.gz
```

4.) Create a new release on GitHub with the new binary archive

Make sure to manually add the created python package to the release.
