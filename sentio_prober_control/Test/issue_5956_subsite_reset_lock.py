from sentio_prober_control.Sentio.ProberSentio import *
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp


def main():

    try:
        # create a communication object
        comm_tcp_ip = CommunicatorTcpIp()
        comm_tcp_ip.connect("127.0.0.1:35555")

        # Query idn to check communication
        prober = SentioProber(comm_tcp_ip)
        prober.select_module(Module.Wafermap)

        map = prober.map
        map.create(300)
        map.set_grid_params(5000, 5000, 0, 0, 4000)
        map.set_grid_origin(0, 0)
        map.set_home_die(0, 0)

        for i in range(1, 1000):
            print(f"iteration counter {i}")
            map.subsites.reset()
            map.subsites.add('site_2', 1000, 1000, AxisOrient.UpRight)
            map.subsites.add('site_3', 2000, 2000, AxisOrient.UpRight)

        print("Success!")

    except ProberException as e:
        print("\n#### Error ##################################")
        print("{0}".format(e.message()))


if __name__ == "__main__":
    main()