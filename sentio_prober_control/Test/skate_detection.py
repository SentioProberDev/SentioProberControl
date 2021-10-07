import os

from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
import time

#
# This example will demonstrate different tip detection methods
# required SENTIO Version: 3.6.0 or higher
#

def check_preconditions(prober):
    # 1.) Check whether the machine has a motorized chuck.
    if (not prober.vision.has_camera(CameraMountPoint.Scope)):
        raise Exception("This script requires a scope camera in order to run!")


def main():
    try:
        script_path = os.path.dirname(os.path.realpath(__file__))

        comm : CommunicatorTcpIp= CommunicatorTcpIp.create("127.0.0.1:35555")
        prober: SentioProber = SentioProber(comm)

        check_preconditions(prober)

        prober.select_module(Module.Vision)
        prober.vision.switch_camera(CameraMountPoint.Scope)
        comm.send("*DEMO_IMAGE scope, wizard_skate_detection\step3_cont.jpg")
        resp = prober.send_cmd("vis:sd:find_initial_setup scope, east,west")
        resp.dump()

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()