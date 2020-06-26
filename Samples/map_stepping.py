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

        x, y, z, t = prober.move_chuck_site(ChuckSite.Wafer)
        print("absolute chuck position is x={0}; y={1}; z={2}; theta={3}°".format(x, y, z, t))

        hasHome, hasContact, overtravelActive, vacuumOn = prober.get_chuck_site_status(ChuckSite.Wafer)

        if not hasHome:
            raise Exception("Home position must be set to execute this script!")

        if not hasContact:
            raise Exception("Contact must be set for stepping!")



        prober.select_module(Module.Wafermap)

        # setup a wafermap
        prober.map.create(200)
        prober.map.set_flat_params(90, 50000)
        prober.map.set_grid_params(15000, 15000, 0, 0, 1000)
        prober.map.set_street_size(0, 0)
        prober.map.set_grid_origin(0, 0)
        prober.map.set_home_die(1, 1)
        prober.map.set_axis_orient(AxisOrient.UpRight)
        prober.map.set_color_scheme(ColorScheme.ColorFromBin)

        prober.map.bins.load("C:\ProgramData\MPI Corporation\Sentio\config\defaults\default_bins.xbt")
        prober.map.bins.clear_all()

        prober.map.path.select_dies(TestSelection.All)
        prober.map.path.set_routing(RoutingStartPoint.UpperRight, RoutingPriority.ColBiDir)

        # do the stepping
        crs = prober.map.step_first_die()
        print("Position {0}, {1} (Site: {2})".format(crs[0], crs[1], crs[2]))

        bin_value = 3

        #
        # Stepping Version 1: Use the EndOfRoutException as the abort criteria
        #

#        try:
#            while True:
#                crs = prober.map.bin_step_next_die(bin_value)
#                # crs = prober.step_next_die()
#                print("Position {0}, {1} (Site: {2})".format(crs[0], crs[1], crs[2]))
#        except ProberException as e:
#            print(e.message())

        #
        # Stepping Version 2: Manually check end of route
        #

        while True:
            if not prober.map.end_of_route():
                crs = prober.map.bin_step_next_die(bin_value)
                #crs = prober.map.step_next_die()
                print("Position {0}, {1} (Site: {2})".format(crs[0], crs[1], crs[2]))
            else:
                prober.map.bins.set_bin(bin_value, crs[0], crs[1])
                print("Last Die {0}, {1} (Site: {2})".format(crs[0], crs[1], crs[2]))
                break

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()