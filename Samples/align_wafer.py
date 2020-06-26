import os

from Mpi.Sentio.ProberSentio import *
from Mpi.Communication.CommunicatorGpib import *
from Mpi.Communication.CommunicatorTcpIp import *


def main():

    try:
#        prober = SentioProber(CommunicatorGpib.create(GpibCardVendor.Adlink, "GPIB0:20"))
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))
        prober.select_module(Module.Wafermap)

        # open a project
        # - must have contact height set
        # - must have a home position set
        # - align_wafer must be set up properly
        # - focus height should be set in the project

        project = os.path.dirname(os.path.abspath(__file__)) + "\projects\sample_align"
        prober.open_project(project)
        prober.select_module(Module.Vision)

        x, y = prober.move_chuck_home()
        print("Chuck at home position (x={0}, y={1} um)".format(x, y))

        z = prober.move_chuck_separation()
        print("Chuck at separation (z={0} um)".format(z))

        # bring scope down to the old focus height. This is probably close to focus,
        # but not exactly the focus height
        prober.vision.auto_focus(AutoFocusCmd.GoTo)

        # Do an autofocus to nail the focus height
        prober.vision.auto_focus(AutoFocusCmd.Focus)

        # perform wafer alignment
        prober.vision.align_wafer()

        home, contact, overtravel, vacuum = prober.get_chuck_site_status(ChuckSite.Wafer)

        t = prober.get_chuck_theta(ChuckSite.Wafer)
        print("Chuck alignment angle is {0} Deg".format(t))

    except ProberException as e:
        print("\n#### Error ##################################")
        print("{0}".format(e.message()))


if __name__ == "__main__":
    main()