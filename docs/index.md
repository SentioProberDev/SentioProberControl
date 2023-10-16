# Sentio Prober Control Documentation

![AST_Back_2A fw_](https://user-images.githubusercontent.com/2202567/204108957-0c7a864a-a526-4d32-a1ca-51985a0b01c6.png)

## Installation

The package for controlling MPI probe stations running the MPI SENTIO Software suite is available via [pythons package index](https://pypi.org/project/sentio-prober-control/). To install the
package simply type:

```python -m pip install sentio-prober-control```

## Overview

All functionality is accessed via an object of type [SentioProber](SentioProber.md) . You should only have a single instance of this class in your 
python script. Naturally a script should start with initializing the prober.

### Initialization

The following minimal example creates an instance of the prober class and initializes it for TCP/IP communication with a 
SENTIO running on the local PC on port 35555:

```python
from sentio_prober_control.Sentio.ProberSentio import *
prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
prober.select_module(Module.Wafermap)
```

Some functionality is provided directy via member functions of the ProberSentio class. Functionality of SENTIO modules
can be accessed via the [module attributes](SentioProber.md) class. 

### A first example

The following example will set up a wafer map. [Wafermap functionality](WafermapCommandGroup.md) is accessed via the map attribute of the prober class.

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
		