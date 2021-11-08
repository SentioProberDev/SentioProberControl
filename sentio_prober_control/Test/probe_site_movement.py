from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Sentio.Enumerations import *


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

    for i in range(1, len(subsiteListEastX)+1):
        prober.probe.move_probe_xy(ProbeSentio.East, ProbeXYReference.Home, subsiteListEastX[i],  subsiteListEastY[i])
        prober.probe.move_probe_xy(ProbeSentio.West, ProbeXYReference.Home, subsiteListWestX[i],  subsiteListWestY[i])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n#### Error ####")
        print("{0}".format(e))
