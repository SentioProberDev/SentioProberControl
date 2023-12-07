import pyvisa

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase


class CommunicatorVisa(CommunicatorBase):
    """Communicator for VISA communication.

    This communicator is meant for communication over National Instruments VISA interface.
    In order to use it you must have the [NI-VISA driver](https://www.ni.com/de/support/downloads/drivers/download.ni-visa.html) installed on your system.
    """

    def __init__(self):
        """Constructs a VISA communicator."""
        self.__rm = pyvisa.ResourceManager()

    @staticmethod
    def create(addr: str):
        """Create an instance of a VISA communicator.

        :param addr: A string that specifies the address of the VISA device to connect to. The address must be a valid VISA resource identifier.
        """
        c = CommunicatorVisa()
        c.connect(addr)
        return c

    def connect(self, address: str):
        """Connect to a VISA device at the specified address.

        The VISA timeout for the interface is set to 3600000 (1 hour).

        :param addr: A string that specifies the address of the VISA device to connect to. The address must be a valid VISA resource identifier.
        """
        self.__visa = self.__rm.open_resource(address)
        self.__visa.timeout = 3600000

    def disconnect(self):
        """Disconnect from the VISA device."""
        if CommunicatorBase._verbose:
            print("Diconnecting comunicator to {0}".format(self.__address))

        self.__visa.close()

    def send(self, msg: str):
        """Send a command to the VISA device.

        :param msg: The command to send.
        """
        if CommunicatorBase._verbose:
            print('Sending "{0}"'.format(msg))

        self.__visa.write((msg + "\n"))

    def read_line(self):
        """Read a line from the VISA device.

        :return: The read line.
        """
        return self.__visa.read()
