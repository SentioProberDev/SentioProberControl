from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Sentio.Enumerations import *

#-------------------------------------------------------#
# Example for SiPH Probe with Stepping
#-------------------------------------------------------#
def main():
    # Prepare communication
    prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

    # 1. Load subsite table
    subsiteListEastX = {
        1: 0,
        2: 50,
        3: 100,}
    subsiteListEastY = {
        1: 0,
        2: 50,
        3: 100,}

    subsiteListWestX = {
        1: 0,
        2: -50,
        3: -100,}
    subsiteListWestY = {
        1: 0,
        2: 50,
        3: 100,}

    prober.siph.move_separation(ProbeSentio.East)
    prober.siph.move_separation(ProbeSentio.West)

    prober.probe.move_probe_home(ProbeSentio.East)
    prober.probe.move_probe_home(ProbeSentio.West)

    prober.move_chuck_separation()

    prober.move_chuck_home()
    prober.move_chuck_contact()

    prober.siph.move_siph_hover('East')
    prober.siph.move_siph_hover('West')
    prober.siph.siph_fast_alignment()

    prober.map.step_first_die()

    for j in range(1, len(subsiteListEastX) + 1):
        prober.probe.move_probe_xy(ProbeSentio.East, ProbeXYReference.Home, subsiteListEastX[j], subsiteListEastY[j])
        prober.probe.move_probe_xy(ProbeSentio.West, ProbeXYReference.Home, subsiteListWestX[j], subsiteListWestY[j])

        prober.move_chuck_contact()

        prober.siph.move_siph_hover('East')
        prober.siph.move_siph_hover('West')

        prober.siph.gradient_search()

        #---Measurement---#

    die_num = prober.map.get_num_dies(DieNumber.Selected)  # Get total dies
    for i in range(1, int(die_num)):
        prober.siph.move_separation(ProbeSentio.East)
        prober.siph.move_separation(ProbeSentio.West)

        prober.map.move_next_die()

        # 13-3. ProbeSubsite_nextdie
        for j in range(1, len(subsiteListEastX) + 1):
            prober.probe.move_probe_xy(ProbeSentio.East, ProbeXYReference.Home, subsiteListEastX[j],
                                       subsiteListEastY[j])
            prober.probe.move_probe_xy(ProbeSentio.West, ProbeXYReference.Home, subsiteListWestX[j],
                                       subsiteListWestY[j])
            prober.move_chuck_contact()

            prober.siph.move_siph_hover('East')
            prober.siph.move_siph_hover('West')

            prober.siph.gradient_search()

            # ---Measurement---#


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n#### Error ####")
        print("{0}".format(e))
