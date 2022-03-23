from operator import truediv
import time

from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorGpib import *
from sentio_prober_control.Communication.CommunicatorTcpIp import *


def main():

    try:
        #        prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))
        prober.initialize_if_needed()
        
        # Use Sentios mechanism for sending remote commands directly
        # Start first command
        resp: Response = prober.send_cmd("start_async_cmd")
        cmd_id1: int = resp.cmd_id()

        # Start second command
        resp = prober.send_cmd("start_async_cmd")
        cmd_id2 = resp.cmd_id()

        #
        # Her you can do other stuff whilst the commands are executing
        #

        # Method 1:
        # Wait for all commands to finish
        prober.wait_all(180)
        # alternatively wait for each of the commands:
        #prober.wait_complete(cmd_id1, 60)
        #prober.wait_complete(cmd_id2, 60)

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