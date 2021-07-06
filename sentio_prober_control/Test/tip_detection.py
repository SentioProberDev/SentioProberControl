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

        ###########################################################################################
        #
        # Scope Camera
        #
        ###########################################################################################

        prober.vision.switch_camera(CameraMountPoint.Scope)
        comm.send("*DEMO_IMAGE scope, scope_celadon_10x.jpg")

        #
        # Keypoint Detector:
        # A generic detector originally designed for automatic stitching of panoramic images.
        # Will snap to Edges and high contrast areas.
        #
        prober.vision.detect_probetips(CameraMountPoint.Scope, ProbeTipDetector.Keypoint)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        #
        # Probe tip Detector:
        # A haar cascade based detector trained on tip images seen from above.
        #

        prober.vision.detect_probetips(CameraMountPoint.Scope, ProbeTipDetector.ProbeTip)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        #
        # Experimental:  Detector for titan heads in north orientation:
        # A haar cascade based detector trained on images of titan heads (in north position only!)
        #

        comm.send("*DEMO_IMAGE scope, titan_heads_5x.jpg")
        prober.vision.detect_probetips(CameraMountPoint.Scope, ProbeTipDetector.TitanHead)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        #
        # Experimental:  Detector for titan tips:
        # A haar cascade based detector trained on images of titan tips
        #

        prober.vision.detect_probetips(CameraMountPoint.Scope, ProbeTipDetector.TitanTip)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        ###########################################################################################
        #
        # Chuck Camera
        #
        ###########################################################################################

        prober.vision.switch_camera(CameraMountPoint.Chuck)
        comm.send("*DEMO_IMAGE chuck, probe_tips_bottom.jpg")

        #
        # Keypoint Detector:
        # A generic detector originally designed for automatic stitching of panoramic images.
        # Will snap to Edges and high contrast areas.
        #

        prober.vision.detect_probetips(CameraMountPoint.Chuck, ProbeTipDetector.Keypoint)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        #
        # Probe tips from below:
        # A haar cascade based detector trained on images of tips seen and illuminated from below
        #

        prober.vision.detect_probetips(CameraMountPoint.Chuck, ProbeTipDetector.ProbeTipFromBelow)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        #
        # PyramidTipRingLight Detector:
        # A haar cascade based detector trained on images with pyramid tips as seen from the chuck camera and
        # illuminated with the ring light
        #

        comm.send("*DEMO_IMAGE chuck, pyramide_tips_ring.jpg")
        prober.vision.detect_probetips(CameraMountPoint.Chuck, ProbeTipDetector.PyramidTipRingLight)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

        #
        # PyramidTipSpotLight Detector:
        # A haar cascade based detector trained on images with pyramid tips as seen from the chuck camera and
        # illuminated with the spot light
        #

        comm.send("*DEMO_IMAGE chuck, pyramide_tips_spot.jpg")
        prober.vision.detect_probetips(CameraMountPoint.Chuck, ProbeTipDetector.PyramidTipSpotLight)
        time.sleep(2)
        prober.vision.remove_probetip_marker()

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()