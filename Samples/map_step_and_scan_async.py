import os
import random

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

        prober.open_project(os.path.dirname(os.path.abspath(__file__)) + "\projects\sample_round")
        prober.select_module(Module.Wafermap)
        prober.map.set_color_scheme(ColorScheme.ColorFromBin)
        prober.move_chuck_home()

        resp = prober.loader.start_prepare_station(LoaderStation.Cassette1)
        prep_stat_cmd_id = resp.cmd_id()

        try:
            pass
            crs = prober.map.step_first_die()
            print("Position {0}, {1} (Site: {2})".format(crs[0], crs[1], crs[2]))

            while True:
                crs = prober.map.bin_step_next_die(random.randint(1,3))
                print("Position {0}, {1} (Site: {2})".format(crs[0], crs[1], crs[2]))

        except ProberException as e:
            print(e.message())

        finally:
            # the scan should terminate longe before the stepping ends.
            # this function will get the response.
            #
            # Note:
            # You MUST call waitcomplete or query_command_status. Async commands
            # are not "fire and forget" commands. For each async command you have
            # to collect the response! Otherwise responses will pile up inside SENTIO!
            prober.wait_complete(prep_stat_cmd_id, 86400)

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()