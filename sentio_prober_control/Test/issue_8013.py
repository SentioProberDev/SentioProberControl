import os

from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
import time

#
# This example will demonstrate on-axis ptpa
#

def check_preconditions(prober):
    # 1.) Check whether the machine has a motorized chuck.
    if (not prober.has_chuck_xyz()):
        raise Exception("This script requires a motorized chuck in order to run!")

    # 2.) Check whether the home position of the chuck wafer site is set
    hasHome, hasContact, overtravelActive, vacuumOn = prober.get_chuck_site_status(ChuckSite.Wafer)
    if (not hasHome):
        raise Exception("Home position is not set!")

    if (not hasContact):
        raise Exception("Contact height is not set!")

    hasHomePattern = prober.vision.camera.is_pattern_trained(CameraMountPoint.Scope, DefaultPattern.Home)
    if (not hasHomePattern):
        raise Exception("The home pattern is not trained. FindHome will not work!")

def main():

    try:
        prober: SentioProber = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        check_preconditions(prober)

        script_path = os.path.dirname(os.path.realpath(__file__))
        projectPath: str = prober.get_project(ProjectFileInfo.FullPath)
        print(f'Project path: {projectPath}')

        prober.file_transfer('C:\\Users\\berg\\Desktop\\WaferTracking.pptx', 'C:\\Users\\berg\\Desktop\\foobar.pptx')

        # align wafer, find home and determine contact through PTPA alignment
        prober.move_chuck_home()
        prober.move_chuck_separation()

        #prober.vision.align_wafer()
        prober.vision.find_home()
        prober.move_chuck_contact()

        # check alignment
        time.sleep(5)
        prober.vision.get_prop('ptpa_onaxis.xyz_offset')
#        prober.send_cmd("vis:get_prop ptpa_onaxis.xyz_offset")
        time.sleep(1)

        # step Sentio map and measure
        prober.map.step_first_die()
        prober.move_chuck_contact()

        index = 0
        while True:
            # measure
            time.sleep(3)
            prober.vision.get_prop('ptpa_onaxis.xyz_offset')
            time.sleep(1)

            # move to next die, stop if at last die
            try:
                prober.map.step_next_die()
                prober.move_chuck_contact()
            except ProberException as e:
                break
            index = index + 1

        # separate and unload when done
        prober.move_chuck_separation()

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()