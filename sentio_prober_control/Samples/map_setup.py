from Mpi.Devices.Enumerations import GpibCardVendor
from Mpi.Sentio.ProberSentio import *
from Mpi.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from Mpi.Communication.CommunicatorGpib import CommunicatorGpib


def main():

    try:

        #       Setup GPIB Communication
#        prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))

        #       Setup TCPIP Communication
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

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

        for i in range(1,4):
            for j in range(1, 5):
                map.die.remove(4+i, 4+j)
                map.die.remove(-10+i, 4+j)

        for i in range(-7, 7):
            if abs(i) > 6:
                map.die.remove(i, -8)
            elif abs(i) > 4:
                map.die.remove(i, -9)
            else:
                map.die.remove(i, -10)

        # read map data
        print("Wafermap diameter: {0} mm".format(map.get_diameter()))
        print("Grid axis orientation: {0}".format(map.get_axis_orient()))
        print("Grid origin: {0}".format(map.get_grid_origin()))
        print("Index size: {0}".format(map.get_index_size()))
        print("Street Size: {0}".format(map.get_street_size()))
        print("present dies: {0}".format(map.get_num_dies(DieNumber.Present)))
        print("Selected dies: {0}".format(map.get_num_dies(DieNumber.Selected)))

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))

if __name__ == "__main__":
    main()