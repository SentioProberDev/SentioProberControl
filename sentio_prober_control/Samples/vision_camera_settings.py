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

        prober.vision.camera.set_light(CameraMountPoint.Scope, 200)
        light_val: int = prober.vision.camera.get_light(CameraMountPoint.Scope)
        print("Light: {0}".format(light_val))

        prober.vision.camera.set_exposure(CameraMountPoint.Scope, 100)
        exposure_val: int = prober.vision.camera.get_exposure(CameraMountPoint.Scope)
        print("Exposure: {0}".format(exposure_val))

        prober.vision.camera.set_gain(CameraMountPoint.Scope, 5)
        gain_val: int = prober.vision.camera.get_gain(CameraMountPoint.Scope)
        print("Gain: {0}".format(gain_val))

    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))


if __name__ == "__main__":
    main()