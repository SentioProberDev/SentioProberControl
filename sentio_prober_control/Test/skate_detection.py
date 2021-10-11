import os

from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
import time

#
# This example will demonstrate different tip detection methods
# required SENTIO Version: 3.6.0 or higher
#

def check_preconditions(prober: SentioProber):
    # 1.) Check whether the machine has a motorized chuck.
    if (not prober.vision.has_camera(CameraMountPoint.Scope)):
        raise Exception("This script requires a scope camera in order to run!")

def train_initial_setup(prober: SentioProber):
        prober.select_module(Module.Vision)
        prober.vision.switch_camera(CameraMountPoint.Scope)
        prober.comm.send("*DEMO_IMAGE scope, wizard_skate_detection\step3_cont.jpg")

        resp = prober.send_cmd("vis:sd:find_initial_setup scope, east,west")
        resp.dump()

def test_offset_loop(prober: SentioProber):

    chuckx, chucky = prober.get_chuck_xy(ChuckSite.Wafer, ChuckXYReference.Zero)
    print(f"Initial chuck position: {chuckx}, {chucky}")

    try:
        while True:
            resp = prober.send_cmd("vis:sd:find_offset scope, true")
            if not resp.ok:
                raise Exception("vis:sd:find_offset error!")

            tok = resp.message().split(",")
            print(f"offset: {float(tok[0])}, {float(tok[1])}")
    except KeyboardInterrupt:
        pass

def main():
    try:
        script_path = os.path.dirname(os.path.realpath(__file__))

        comm : CommunicatorTcpIp= CommunicatorTcpIp.create("127.0.0.1:35555")
        prober: SentioProber = SentioProber(comm)

        check_preconditions(prober)

        #
        # Training of the setup (probes in pad contact, models need to be trained)
        #

        # train_initial_setup(prober)

        prober.open_project("C:\\ProgramData\\MPI Corporation\\SENTIO\\projects\\test_skate_detection", True)
        prober.move_chuck_z(ChuckZReference.Separation, 0)

        prober.vision.auto_focus(AutoFocusCmd.GoTo)

        # I have titan tips in the FOV, move scope away
        prober.vision.align_wafer(120000)
        prober.vision.find_home()

        prober.select_module(Module.Vision)

        # for this implementation stepping mode must be set to Step to separation. Because this script will
        # determine the contact height
        prober.vision.set_prop('stepping_mode', 'StepToSeparation')
        col, row, site = prober.map.step_first_die()

        resp1 = prober.send_cmd("vis:sd:find_offset scope, true")
        resp1.check_error()

        resp2 = prober.send_cmd("vis:sd:find_contact scope, update")
        resp2.check_error()

        print(f'{col}, {row}, {site}, {resp1.message()}, {resp2.message()}')

        try:
            while True:
                col, row, site = prober.map.step_next_die()

                resp1 = prober.send_cmd("vis:sd:find_offset scope, true")
                resp1.check_error()
               
                resp2 = prober.send_cmd("vis:sd:find_contact scope, update")
                resp2.check_error()

                print(f'{col}, {row}, {site}, {resp1.message()}, {resp2.message()}')
        except ProberException as e:
            if e.error() != RemoteCommandError.EndOfRoute:
                raise  

#        test_offset_loop(prober)

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()