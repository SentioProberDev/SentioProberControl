import time
from Mpi.Sentio.ProberSentio import *
from Mpi.Communication.CommunicatorGpib import *
from Mpi.Communication.CommunicatorTcpIp import *


def main():

    try:
        #        prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))
        prober.initialize_if_needed()

        # Use Sentios mechanism for sending remote commands directly
        resp: Response = prober.send_cmd("start_async_cmd")
        cmd_id: int = resp.cmd_id()

        # There are two ways to ways to wait for asynchronous commands:
        # First way, use blocking wait_complete call. (Second parameter is the timeout)
        prober.wait_complete(cmd_id, 60)

        # Second way use query_command_status for polling:
        #while True:
        #    time.sleep(1)
        #    resp = prober.query_command_status(cmd_id)
        #    if (resp.errc()!=RemoteCommandError.CommandPending):
        #        break;

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()