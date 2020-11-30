from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp

#
# This example will demonstrate how to navigate the chuck with a point of interest list (POI)
#
# This script will set up a list with POI spread across the die. It will then use the chuck to step
# over all POI in the list for all active dies
#

# Required Preconditions to run this script
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

    # IMPORTANT:
    # The POI MUST be inside of the Die! If you set up POI at the edge of the wafer you may experience undefined
    # behavior! Here is why:
    #   - If you place a poi on a die edge it cannot be assigned to a specific die because its
    #     position is ambiguous!
    #   - The chuck can be positioned only with +/- 1-2 µm accuracy. This are has to be avoided when setting poi's!
    #   - Sentio is using the chuck position to determine the current die. If the chuck is closer than 1 µm to a die edge
    #     SENTIO may incorrectly determin it is in the neighboring die due to limited chuck accuracy!
    #   - I avoid the entire trouble by assuming the die is slightly smaller than it really is.
    sx = sx - 4  # 2 µm on the sides of the die are the poi "no go" zone
    sy = sy - 4  # 2 µm on the sides of the die are the poi "no go" zone

    die_center_x = sx / 2
    die_center_y = sy / 2

    # Create this many rows and columns of POI. You can change the number is you like but
    # use an odd number!
    ncols = 3
    nrows = 3

    dx = sx / (ncols-1)
    dy = sy / (nrows-1)

    print("Creating {0} points of interest:".format(ncols * nrows))

    # Set up a poi map for the chuck which i using the die center as a reference position
    prober.map.poi.reset(Stage.Chuck, PoiReferenceXy.DieCenter)

    ct = 0
    for r in range(-nrows//2, nrows//2):
        for c in range(-ncols//2, ncols//2):
            ct = ct + 1
            poi_x = die_center_x + c * dx
            poi_y = die_center_y + r * dy
            print("Poi {0} at {1}, {2} µm".format(ct, poi_x, poi_y))
            prober.map.poi.add(poi_x, poi_y, "poi_{0}".format(ct))

def main():

    try:
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        check_preconditions(prober)
        set_poi(prober)

        # Stepping loop:
        # - Step over all active dies. For each die step over all poi
        # - for this example we will NOT go into contact!
        prober.map.path.select_dies(TestSelection.All)
        prober.map.path.set_routing(RoutingStartPoint.UpperRight, RoutingPriority.ColBiDir)

        num_poi = prober.map.poi.get_num()
        prober.map.step_first_die()

        selected_poi = [ 'poi_1', 'poi_5', 'poi_9']
        while True:
            # Variant 1: Step over all POI (comment Variant 2 to us this)
            selected_poi = range(0, num_poi)

            # Variant 2: Step over all POI
            selected_poi = [ 'poi_1', 'poi_5', 'poi_9']

            # Do the poi stepping
            for i in selected_poi:
                prober.map.poi.step(i)

            # Step to the next die
            prober.map.step_next_die()
            if prober.map.end_of_route():
                break

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()