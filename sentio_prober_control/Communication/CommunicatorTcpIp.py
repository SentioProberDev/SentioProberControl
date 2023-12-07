import socket

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase


class CommunicatorTcpIp(CommunicatorBase):
    """Communicator for TCP/IP communication."""

    def __init__(self):
        """Construcst a TCP/IP communicator."""
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    @staticmethod
    def create(addr: str):
        """Create an instance of a TCP/IP communicator.

        :param addr: A string that specifies the address of the TCP/IP device to connect to. The address must have the format "IP_ADDRESS&colon;PORT"
        """
        c = CommunicatorTcpIp()
        c.connect(addr)
        return c

    def connect(self, address: str):
        """Connect to a TCP/IP device at the specified address.

        :param addr: A string that specifies the address of the TCP/IP device to connect to. The address must have the format "IP_ADDRESS&colon;PORT"
        """
        tok = address.split(":")
        self.__address = tok[0]
        self.__port = int(tok[1])

        if CommunicatorBase._verbose:
            print(
                "Connecting comunicator to {0}:{1}".format(self.__address, self.__port)
            )

        self.__socket.connect((self.__address, self.__port))

    def disconnect(self):
        """Disconnect from the TCP/IP device."""
        if CommunicatorBase._verbose:
            print("Diconnecting comunicator to {0}".format(self.__address))

        self.__socket.close()

    def send(self, msg: str):
        """Send a command to the TCP/IP device.

        :param msg: The command to send.
        """

        if CommunicatorBase._verbose:
            print('Sending "{0}"'.format(msg))

        self.__socket.send((msg + "\n").encode())

    def read_line(self):
        """Read a line from the TCP/IP device.

        :return: The read line.
        """
        return self.__socket.makefile().readline().rstrip()
