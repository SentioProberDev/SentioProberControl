from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase
from sentio_prober_control.Communication.CommunicatorGpib import *
from sentio_prober_control.Communication.CommunicatorTcpIp import *


def main():

    try:
        CommunicatorBase._verbose = False
#        ProberSentio._verbose = False

#       Setup GPIB Communication
#        prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))

#       Setup TCPIP Communication
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        num = prober.map.subsites.get_num();
        print("Number of subsites: {0}".format(num))

        for i in range(0, num):
            desc, x, y = prober.map.subsites.get(i)
            print("Subsite {0}: desc={1}, x={2}, y={3}".format(i, desc, x, y))

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))

if __name__ == "__main__":
    main()