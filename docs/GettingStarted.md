# Getting Started

## Installation

The package for controlling MPI probe stations running the MPI SENTIO Software suite is available via [pythons package index](https://pypi.org/project/sentio-prober-control/). To install the
package simply type:

```py -m pip install sentio-prober-control```


## Example

``` py
from sentio_prober_control.Sentio.ProberSentio import *


def main():

    try:
        prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
        prober.select_module(Module.Wafermap)

        # setup a wafermap
        map = prober.map
        map.create(200)

        map.set_flat_params(180, 50000)
        map.set_grid_params(5000, 5000, 0, 0, 4000)
        map.set_street_size(0, 0)
        map.set_axis_orient(AxisOrient.UpRight)
        map.set_grid_origin(1, 2)
        map.set_home_die(0, 0)
        map.set_color_scheme(ColorScheme.ColorFromBin)

        map.path.select_dies(TestSelection.All)
        map.bins.set_all(3, BinSelection.All)
        map.bins.load("C:\ProgramData\MPI Corporation\Sentio\config\defaults\default_bins.xbt")

        print(f"Wafermap diameter: {map.get_diameter()} mm")
        print(f"Grid axis orientation: {map.get_axis_orient()}")
        print(f"Grid origin: {map.get_grid_origin()}")
        print(f"Index size: {map.get_index_size()}")
        print(f"Street Size: {map.get_street_size()}")
        print(f"present dies: {map.get_num_dies(DieNumber.Present)}")
        print(f"Selected dies: {map.get_num_dies(DieNumber.Selected)}")

        prober.local_mode()
    except Exception as e:
        print("\n#### Error ##################################")
        print(f"{e}")

if __name__ == "__main__":
    main()
```
		

## Overview

The SentioProber class is your gateway to control a probe station running the MPI SENTIO 
Software suite.

Some functionality is provided directy via member functions of the class.
The following example triggers a switch of the active SENTIO module by using the 
select_module function:

```python
from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp

prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))
prober.select_module(Module.Wafermap)
```