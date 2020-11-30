from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp

#
# This example will demonstrate how to navigate the chuck with a point of interest list (POI)
#
# This script will set up a list with POI spread across the die. It will then use the chuck to step
# over all POI in the list
#
# Preconditions:
#    - You need a system with a motorized chuck
#    - a chuck home position must be set
#

def check_preconditions(prober):
    # 1.) Check whether the machine has a motorized chuck.
    if (not prober.has_chuck_xyz()):
        raise Exception("This script requires a motorized chuck in order to run!")

    # 2.) Check whether the home position of the chuck wafer site is set
    hasHome, hasContact, overtravelActive, vacuumOn = prober.get_chuck_site_status(ChuckSite.Wafer)
    if (not hasHome):
        raise Exception("Home position must be set to execute this script!")

    # 3.) Check whether the die reference position is set.
    # This script requires a valid die reference position. The die reference position is the distance from the corner
    # of the die to the pad. Only when it is set can SENTIO know where the pad is located inside the die.
    if (not prober.map.die_reference_is_set()):
        raise Exception("The die reference position is not trained! Sentio cannot know where the home position is located inside the die exactly!")

#
# Distribute 9 POI across the die. The POI layout will look like shown here:
#
#      1-------------2-------------3
#      |                           |
#      |                           |
#      |                           |
#      |                           |
#      |                           |
#      4             5             6
#      |                           |
#      |                           |
#      |                           |
#      |                           |
#      |                           |
#      7-------------8-------------9
#
# - Numbers indicate the POI index and their position.
# - POI number 5 is at the center of the die
def set_poi(prober):
    # 1.) get the die Size
    sx, sy = prober.map.get_index_size()
    print("Die size is {0}, {1} µm".format(sx, sy))

    die_center_x = sx / 2
    die_center_y = sy / 2

    # Create this many rows and columns of POI. You can change the number is you like but
    # use an odd number!
    ncols = 3
    nrows = 3

    dx = sx / (ncols-1)
    dy = sy / (nrows-1)

    print("Creating {0} points of interest:".format(ncols * nrows))

    # Compute the POI Positions relative to the die center.
    prober.map.poi.reset();

    ct = 0
    for r in range(-nrows//2, nrows//2):
        for c in range(-ncols//2, ncols//2):
            ct = ct + 1
            poi_x = die_center_x + c * dx
            poi_y = die_center_x + r * dy
            print("Poi {0} at {1}, {2} µm".format(ct, poi_x, poi_y))
            prober.map.poi.add(poi_x, poi_y, "poi_{ct}".format(ct))

def main():

    try:
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        check_preconditions(prober)
        set_poi(prober)

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()