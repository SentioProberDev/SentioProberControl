from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
import time

#
# This example will demonstrate how to navigate the chuck with a point of interest list (POI)
#
# This script will set up a list with POI spread across the die. It will then use the chuck to step
# over all POI in the list for all active dies
#

# Check preconditions required to reproduce #6947
def check_preconditions(prober):
    if (not prober.has_chuck_xyz()):
        raise Exception("This script requires a motorized chuck in order to run!")

    hasHome, hasContact, overtravelActive, vacuumOn = prober.get_chuck_site_status(ChuckSite.Wafer)
    if (not hasHome):
        raise Exception("Home position must be set to execute this script!")



def main():

    try:
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        check_preconditions(prober)
        prober.aux.cleaning.enable_auto(False);
        prober.set_stepping_contact_mode(SteppingContactMode.BackToContact)

        prober.move_chuck_site(ChuckSite.Wafer)
        prober.map.step_first_die()
        prober.move_chuck_contact()

        ct = 0
        while True:
            prober.map.step_next_die()
            ct = ct + 1
            if (ct % 3) == 0:
                # root cause of the issue is that SENTIO will reset the active die when the hchuck is moved to
                # the aux site home position
                prober.move_chuck_site(ChuckSite.AuxRight)
                prober.move_chuck_home()
                prober.move_chuck_site(ChuckSite.Wafer)

                # workflow that does not show the error:
                #prober.aux.cleaning.start(1)

            #time.sleep(0.3)
            if prober.map.end_of_route():
                break

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()