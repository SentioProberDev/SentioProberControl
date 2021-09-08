from sentio_prober_control.Devices.Enumerations import GpibCardVendor
from sentio_prober_control.Devices.GpibAdlinkDriver import *
from sentio_prober_control.Devices.GpibNiDriver import *
from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase;


class CommunicatorGpib(CommunicatorBase):
    def __init__(self, vendor: GpibCardVendor):
        if (vendor==GpibCardVendor.Adlink):
            self._driver = GpibAdlinkDriver()
        elif (vendor==GpibCardVendor.NationalInstruments):
            self._driver = GpibNiDriver()
        else:
            raise NotImplementedError("Driver for Gpib card vendor {0}not implemented!".format(vendor))


    @staticmethod
    def create(vendor: GpibCardVendor, addr: str):
        c = CommunicatorGpib(vendor)
        c.connect(addr)
        return c

    def connect(self, address: str):
        if address is None:
            raise Exception('Gpib address must not be empty!')

        tok = address.split(":")
        if len(tok) != 2:
            raise Exception('Gpib address must have the format "BOARD_NAME:ADDRESS"')

        board: str = tok[0]
        address: int = int(tok[1])
        self._driver.connect(board, address)

    def disconnect(self):
        pass

    def send(self, msg: str):
        self._driver.send(msg)

    def read_line(self):
        return self._driver.receive().rstrip()
