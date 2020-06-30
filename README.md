# Sentio Prober Control - Python Bindings
This archive contains a package with python bindings to control a [MPI Sentio probe station](https://www.mpi-corporation.com/ast/engineering-probe-systems/mpi-sentio-software-suite/).

![](https://www.mpi-corporation.com/wp-content/uploads/2019/12/1.-TS3500-SE-with-WaferWallet_frontview.jpg)

## Instructions for installing the SENTIO prober control module

1.) Download the latest python package from:

https://github.com/SentioProberDev/SentioProberControl/releases

2.) Install the python package with pip:

```python -m pip install sentio_prober_control-0.1.3.tar.gz```

## Instructions for package maintainer (updating the package) 

1.) Install python3

2.) Get the latest version of setuptools and wheel:

```python -m pip install --user --upgrade setuptools wheel```

3.) create the distribution archive:

cd into the archive (where setup.py) is located.

```python setup.py sdist bdist_wheel```

This command will create the dist folder.

```
dist/
  sentio_prober_control-0.1.3-py3-none-any.whl
  sentio_prober_control-0.1.3.tar.gz
```
