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

        #
        # Check whether a loader station exists
        #

        stat = prober.loader.has_station(LoaderStation.WaferWallet)
        if stat:
            print("Station has a Wafer Wallet")

        stat = prober.loader.has_station(LoaderStation.Cassette1)
        if stat:
            print("Station has a Cassette Station 1")

        stat = prober.loader.has_station(LoaderStation.Cassette2)
        if stat:
            print("Station has a Cassette Station 2")

        #
        # Scan the content of a loader station
        #

        slots = prober.loader.scan_station(LoaderStation.Cassette1)
        first_occupied_slot = None
        for i in range(0, len(slots)):
            if (slots[i]=='0'):
                print("Slot {0}: Empty".format(i+1))
            elif (slots[i]=='1'):
                print("Slot {0}: Occupied".format(i + 1))
                if (first_occupied_slot is None):
                    first_occupied_slot = i
            else:
                print("Slot {0}: ERROR".format(i + 1))

        #
        # Move a wafer from the Cassette to the prealigner
        #

        if (not first_occupied_slot is None):
            # mind you: slots are 1 based!
            prober.loader.transfer_wafer(LoaderStation.Cassette1, first_occupied_slot + 1, LoaderStation.PreAligner, 1)

            # prealign the wafer
            prober.loader.prealign(OrientationMarker.Notch, 180)



    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()