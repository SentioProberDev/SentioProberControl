# Getting Started

## Installation

The package for controlling MPI probe stations running the MPI SENTIO Software suite is available via [pythons package index](https://pypi.org/project/sentio-prober-control/). To install the
package simply type:

```py -m pip install sentio-prober-control```

## Overview

All functionality is accessed via an object of type [SentioProber](SentioProber.md) . You should only have a single instance of this class in your 
python script. This class is your gateway to control a probe station running the MPI SENTIO Software suite. Naturally a script 
should start with initializing the prober.

The following minimal example creates an instance of the prober class and triggers a switch of the active SENTIO 
module by using its select_module function:

```python
from sentio_prober_control.Sentio.ProberSentio import SentioProber

prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
prober.select_module(Module.Wafermap)
```

Some functionality is provided directy via member functions of the ProberSentio class. Functionality of SENTIO modules
can be accessed via the [module attributes](SentioProber.md) class. 

## Example

The following example will set up a wafer map. [Wafermap functionality](WafermapCommandGroup.md) is accessed via the map attribute of the prober class.

``` py
from sentio_prober_control.Sentio.ProberSentio import SentioProber


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

## Quickstart

The [SentioProber](/SentioProber/) class is your gateway to control a probe station running the MPI SENTIO 
Software suite. In order to use it you need to create a SentioProber instance.

The following example creates a prober instance and then triggers a switch of the active SENTIO module by 
using the select_module function:

```python
from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp

prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))
prober.select_module(Module.Wafermap)
```