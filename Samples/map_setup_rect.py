from Mpi.Communication.CommunicatorGpib import CommunicatorGpib
from Mpi.Devices.Enumerations import GpibCardVendor
from Mpi.Sentio.ProberSentio import *
from Mpi.Communication.CommunicatorTcpIp import CommunicatorTcpIp


def main():

    try:
        #       Setup GPIB Communication
#        prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))

        #       Setup TCPIP Communication
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        prober.select_module(Module.Wafermap)

        # setup a wafermap
        rows = 10
        cols = 20

        map = prober.map
        map.create_rect(cols, rows)
        map.set_grid_origin(-10, -5)
        map.set_axis_orient(AxisOrient.UpRight)
        map.set_home_die(cols - 1, rows -  1)
        map.set_color_scheme(ColorScheme.ColorFromBin)

        map.path.select_dies(TestSelection.All)
        map.bins.set_all(3, BinSelection.All)

        map.die.remove(0, 0)
        map.die.remove(cols-1, 0)
        map.die.remove(0,rows-1)
        map.die.remove(cols-1, rows-1)

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))

if __name__ == "__main__":
    main()