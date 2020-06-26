from Mpi.Sentio.ProberSentio import *
from Mpi.Communication.CommunicatorTcpIp import CommunicatorTcpIp


def main():

    try:
        #        prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        # Chuck Site Switch
        x, y, z, t = prober.move_chuck_site(ChuckSite.Wafer)
        print("absolute chuck position is x={0}; y={1}; z={2}; theta={3}°".format(x, y, z, t))

        # Chuck Theta Motion
        a = prober.move_chuck_theta(ChuckThetaReference.Relative, 1)
        print("chuck angle is {0}".format(a))

        # Obtain chuck site status information
        hasHome, hasContact, overtravelActive, vacuumOn = prober.get_chuck_site_status(ChuckSite.Wafer)

        prober.select_module(Module.Vision)

        # move chuck to home
        xhome, yhome = prober.move_chuck_home();

        # move chuck relative by 10, 20 µm
        for x in range(-10, 10):
            for y in range(-10, 10):
                # Move Reltive to home:
                prober.move_chuck_xy(ChuckXYReference.Home, 1000 * x, 1000 * y)

                # The same motion as an absolute Motion:
                #prober.move_chuck_xy(ChuckXYReference.Zero, xhome + 1000 * x, yhome + 1000 * y)


    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()