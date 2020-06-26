import random
from Mpi.Sentio.ProberSentio import *
from Mpi.Communication.CommunicatorTcpIp import CommunicatorTcpIp


def main():

        #       Setup TCPIP Communication
        prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))

        # Zero reference test
        prober.vision.imagpro.move_z(IMagProZReference.Center, 0)
        z_init_pos: float = prober.vision.imagpro.get_z(IMagProZReference.Zero)
        prober.vision.imagpro.move_z(IMagProZReference.Zero, z_init_pos + 100)
        z_pos = prober.vision.imagpro.get_z(IMagProZReference.Zero)
        prober.vision.imagpro.move_z(IMagProZReference.Zero, z_init_pos - 100)
        z_pos = prober.vision.imagpro.get_z(IMagProZReference.Zero)

        # Relative reference test
        prober.vision.imagpro.move_z(IMagProZReference.Center, 0)
        z_init_pos = prober.vision.imagpro.get_z(IMagProZReference.Relative)
        prober.vision.imagpro.move_z(IMagProZReference.Relative, z_init_pos + 100)
        z_pos = prober.vision.imagpro.get_z(IMagProZReference.Relative)
        prober.vision.imagpro.move_z(IMagProZReference.Relative, z_init_pos - 100)
        z_pos = prober.vision.imagpro.get_z(IMagProZReference.Relative)

        # Center reference test
        prober.vision.imagpro.move_z(IMagProZReference.Center, 0)
        z_init_pos = prober.vision.imagpro.get_z(IMagProZReference.Center)
        prober.vision.imagpro.move_z(IMagProZReference.Center, z_init_pos + 100)
        z_pos = prober.vision.imagpro.get_z(IMagProZReference.Center)
        prober.vision.imagpro.move_z(IMagProZReference.Center, z_init_pos - 100)
        z_pos = prober.vision.imagpro.get_z(IMagProZReference.Center)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n#### Error ##################################")
        print("{0}".format(e))