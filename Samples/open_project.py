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

        prober.open_project("sample_round")

        # do something...
        prober.map.set_index_size(3333, 4444)

        # save the modified project in Sentio's project folder
        #prober.save_project("my_project")

        # save the project under an absolute path
        prober.save_project("c:\\my_project")

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()