import socket
import locale

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase


class CommunicatorTcpIp(CommunicatorBase):
    """Communicator for TCP/IP communication."""

    def __init__(self):
        """Construcst a TCP/IP communicator."""
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    @staticmethod
    def create(addr: str, encoding : str | None = None) -> CommunicatorBase:
        """Create an instance of a TCP/IP communicator.

            Args: 
                addr (str): A string that specifies the address of the TCP/IP device to connect to. The address must have the format "IP_ADDRESS&colon;PORT"
        """
        c = CommunicatorTcpIp()

        if encoding is None:
            encoding = locale.getpreferredencoding(False)

        c.connect(addr)
        return c

    def connect(self, address: str, encoding : str | None = None) -> None:
        """Connect to a TCP/IP device at the specified address.

            Args:
                address (str): A string that specifies the address of the TCP/IP device to connect to. The address must have the format "IP_ADDRESS&colon;PORT"
                encoding (str|None): The encoding to use for the communication. Default is None.

            Returns:
                None
        """
        tok = address.split(":")
        if len(tok) != 2:
            raise Exception("Invalid address format. Must be IP_ADDRESS:PORT")
        
        self.__address = tok[0]
        self.__port = int(tok[1])

        if CommunicatorBase._verbose:
            print(f"Connecting comunicator to {self.__address}:{self.__port}")

        self.__socket.connect((self.__address, self.__port))

        if encoding is None:
            encoding = locale.getpreferredencoding(False)

        self.__reader = self.__socket.makefile(mode='r', encoding=encoding)

    def disconnect(self):
        """Disconnect from the TCP/IP device."""
        if CommunicatorBase._verbose:
            print(f"Diconnecting comunicator to {self.__address}")

        self.__socket.close()


    def send(self, msg: str):
        """Send a command to the TCP/IP device.

            Args:
                msg (str): The command to send.
        """

        if CommunicatorBase._verbose:
            print(f'Sending "{msg}"')

        self.__socket.send((msg + "\n").encode())

    def read_line(self):
        """Read a line from the TCP/IP device.

            Returns:
                The read line.
        """
        return self.__reader.readline().rstrip()
