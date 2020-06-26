from Mpi.Communication.CommunicatorGpib import CommunicatorGpib
from Mpi.Devices.Enumerations import GpibCardVendor
from Mpi.Sentio.ProberSentio import *
from Mpi.Communication.CommunicatorTcpIp import CommunicatorTcpIp


def main():

    try:
        #       Setup GPIB Communication
#        prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))

        #       Setup TCPIP Communication
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        has_scope_xyz: bool = prober.has_scope_xyz();
        print("Has scope xyz {0}".format(has_scope_xyz))

        has_scope_z: bool = prober.has_scope_z()
        print("Has scope z {0}".format(has_scope_z))

        # move chuck relative by 10, 20 µm
        for x in range(-5, 5):
            for y in range(-5, 5):
                pos_x, pos_y = prober.move_scope_xy(ScopeXYReference.Relative, 100 * x, 100 * y)
                print("move_scope_xy return is {0}, {1}".format(pos_x, pos_y))

                # query scope position without moving
                pos_x, pos_y = prober.get_scope_xy()
                print("get_scope_xy return is {0}, {1}\n".format(pos_x, pos_y))

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()