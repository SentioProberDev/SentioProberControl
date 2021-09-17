from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorGpib import *
from sentio_prober_control.Communication.CommunicatorTcpIp import *


def main():

    try:
        #       Setup GPIB Communication
        #prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))

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
        prober.map.create(100)
        prober.map.set_flat_params(90, 50000)
        prober.map.set_grid_params(15000, 15000, 0, 0, 1000)
        prober.map.set_street_size(0, 0)
        prober.map.set_grid_origin(0, 0)
        prober.map.set_home_die(1, 1)
        prober.map.set_axis_orient(AxisOrient.UpRight)
        prober.map.set_color_scheme(ColorScheme.ColorFromBin)

        # set up 4 subsites
        prober.map.subsites.reset() # This call will create 1 single subsite
        prober.map.subsites.add("site2", 2000, 2000)
        prober.map.subsites.add("site3", 2000, 0)
        prober.map.subsites.add("site4", 0, 2000)

        # Load binning table
        prober.map.bins.load("C:\ProgramData\MPI Corporation\Sentio\config\defaults\default_bins.xbt")
        prober.map.bins.clear_all()

        # Select dies for test
        prober.map.path.select_dies(TestSelection.All)
        prober.map.path.set_routing(RoutingStartPoint.UpperRight, RoutingPriority.ColBiDir)

        #
        # Subsite Stepping Version 1: Stepping over all dies repeatedly for each subsite
        #
        # You don't do subsite stepping. You select the subsite when you submit step_first_die and
        # then do normal wafer stepping. Repeat for each subsite...
        # You step over all dies for each subsite

        num_sites = prober.map.subsites.get_num()

        for testSite in range(0,num_sites):
            col, row, site = prober.map.step_first_die(testSite)  # <- SUBSITE SELECTED HERE!
            print("Position {0}, {1} (Site: {2})".format(col, row, site))

            try:
                while True:
                    bin_value = testSite
                    prober.map.subsites.set_bin(bin_value)

                    col, row, site = prober.map.step_next_die()
                    print(f'Position {col}, {row} (Site: {site})')
            except ProberException as e:
                # An end of route error is normal with this workflow.
                # Everything else will terminate the loop
                if e.error() != RemoteCommandError.EndOfRoute:
                    raise


        #
        # Subsite Stepping Version 2: Use subsite stepping command
        #
        # Step over all sites of the first die, then proceed to the next die.
        # Repeat until all subsites of all dies were measured
        #

        try:
            col, row, site = prober.map.step_first_die()
            bin_value = 0
            while True:
                col, row, site = prober.map.subsites.bin_step_next(bin_value)
                print(f'Position {col}, {row} (Site: {site})')
                bin_value = 0 if site == 0 else bin_value + 1
        except ProberException as e:
            # An end of route error is normal with this workflow.
            # Everything else will terminate the loop
            if e.error() != RemoteCommandError.EndOfRoute:
                raise

    except Exception as e:
        print("\n#### Error ##################################")
        print(e.message())

if __name__ == "__main__":
    main()