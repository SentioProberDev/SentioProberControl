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

    if (not prober.vision.has_camera(CameraMountPoint.Chuck)):
        raise Exception("This script requires a chuck camera in order to run!")


def main():
    try:
        script_path = os.path.dirname(os.path.realpath(__file__))

        comm : CommunicatorTcpIp= CommunicatorTcpIp.create("127.0.0.1:35555")
        prober: SentioProber = SentioProber(comm)

        check_preconditions(prober)

        prober.select_module(Module.Vision)
        prober.vision.switch_camera(CameraMountPoint.Scope)
        comm.send("*DEMO_IMAGE scope, scope_celadon_10x.jpg")
        prober.vision.detect_probetips(CameraMountPoint.Scope, ProbeTipDetector.Keypoint)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        comm.send("*DEMO_IMAGE scope, titan_heads_5x.jpg")
        prober.vision.detect_probetips(CameraMountPoint.Scope, ProbeTipDetector.TitanHead)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        prober.vision.switch_camera(CameraMountPoint.Chuck)
        comm.send("*DEMO_IMAGE chuck, probe_tips_bottom.jpg")
        prober.vision.detect_probetips(CameraMountPoint.Chuck, ProbeTipDetector.ProbeTipFromBelow)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        comm.send("*DEMO_IMAGE chuck, pyramide_tips_ring.jpg")
        prober.vision.detect_probetips(CameraMountPoint.Chuck, ProbeTipDetector.PyramidTipRingLight)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        comm.send("*DEMO_IMAGE chuck, pyramide_tips_spot.jpg")
        prober.vision.detect_probetips(CameraMountPoint.Chuck, ProbeTipDetector.PyramidTipSpotLight)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()