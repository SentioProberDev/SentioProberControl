from enum import Enum

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase
from sentio_prober_control.Devices.GpibAdlinkDriver import GpibAdlinkDriver
from sentio_prober_control.Devices.GpibNiDriver import GpibNiDriver


class GpibCardVendor(Enum):
    """An enumeration that specifies the type of the GPIB card to use for GPIB communication."""

    Adlink = (0,)
    """ Specify this if you use an ADLINK GPIB card. You must have installed the ADLINK drivers on your system in order to use this option! """

    NationalInstruments = 1
    """ Specify this if you use a National Instruments GPIB card. You must have installed the NI-GPIB drivers on your systen in order to use this option! """


class CommunicatorGpib(CommunicatorBase):
    """Communicator for GPIB communication.

    This class is a wrapper around the native GPIB drivers. You can
    use it either with ADLINK or National Instruments GPIB cards.
    The native drivers must be installed on the system or this class
    will not work.
    """

    def __init__(self, vendor: GpibCardVendor):
        """Construcst a GPIB communicator.

        :param vendor: Specifies the native driver to use (either Adlink or NI).
        """
        if vendor == GpibCardVendor.Adlink:
            self._driver = GpibAdlinkDriver()
        elif vendor == GpibCardVendor.NationalInstruments:
            self._driver = GpibNiDriver()
        else:
            raise NotImplementedError(
                "Driver for Gpib card vendor {0}not implemented!".format(vendor)
            )

    @staticmethod
    def create(vendor: GpibCardVendor, addr: str):
        """Create an instance of a GPIB communicator.

        This functions creates an instance of a GPIB communicator and connects it to a given address.

        :param vendor: Specifies the native driver to use (either Adlink or NI)
        :param addr: A string that specifies the address of the GPIB device to connect to. The address must have the format "BOARD_NAME&colon;ADDRESS"
        :return: returns an instance of a GPIB communicator.
        :raises Exception: If the address is empty or does not have the correct format.
        """
        c = CommunicatorGpib(vendor)
        c.connect(addr)
        return c

    def connect(self, address: str):
        """Connects to a GPIB device at the specified address.

        :param addr: A string that specifies the address of the GPIB device to connect to. The address must have the format "BOARD_NAME&colon;ADDRESS"
        :raises Exception: If the address is empty or does not have the correct format.
        """
        if address is None:
            raise Exception("Gpib address must not be empty!")

        tok = address.split(":")
        if len(tok) != 2:
            raise Exception('Gpib address must have the format "BOARD_NAME:ADDRESS"')

        board: str = tok[0]
        address: int = int(tok[1])
        self._driver.connect(board, address)

    def disconnect(self):
        """Disconnects from the GPIB device."""
        pass

    def send(self, msg: str):
        """Send a text string via the communication interface.

        :param msg: The text string to send.
        """
        self._driver.send(msg)

    def read_line(self):
        """Read a line from the communication interface."""
        return self._driver.receive().rstrip()
