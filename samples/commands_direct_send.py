from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorGpib import *
from sentio_prober_control.Communication.CommunicatorTcpIp import *


def main():

    try:
        comm = CommunicatorGpib(GpibCardVendor.Adlink)
        comm.connect("GPIB0:20")

#        comm = CommunicatorTcpIp()
#        comm.connect("127.0.0.1:35555")

        # You can use the communicator to send any command
        comm.send("*IDN?")
        print(comm.read_line())

        # you can also use the prober to send commands
        prober = SentioProber(comm)
        prober.comm.send("*IDN?")
        print(comm.read_line())

        # How to send arbitrary SENTIO remote commands and receive a pre-parsed response object.
        resp = prober.send_cmd("select_module vision")
        resp.dump()

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()