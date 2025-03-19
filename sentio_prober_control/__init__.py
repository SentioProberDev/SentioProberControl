"""  
# SENTIO® Prober Control - Python Bindings
This archive contains a package with python bindings to control a [MPI SENTIO® probe station](https://www.mpi-corporation.com/ast/engineering-probe-systems/mpi-sentio-software-suite/).

![AST_Back_2A fw_](https://user-images.githubusercontent.com/2202567/204108957-0c7a864a-a526-4d32-a1ca-51985a0b01c6.png)

## Installation

The package for controlling MPI probe stations running the MPI SENTIO Software suite is available via [pythons package index](https://pypi.org/project/sentio-prober-control/). 
To install simply type:

```python -m pip install sentio-prober-control```

## Example-Scripts

A set of example scripts for python is maintained in a separate archive at GitHub. 

https://github.com/SentioProberDev/Examples-Python

"""
# from .Sentio.ProberSentio import SentioProber, Module
# from .Communication.CommunicatorTcpIp import CommunicatorTcpIp
# from .Communication.CommunicatorGpib import CommunicatorGpib

print(f"Initializing package {__name__}")

name = "sentio_prober_control"
""" The name of the package. 
    @private
"""
