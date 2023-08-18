import pyvisa

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase;


class CommunicatorVisa(CommunicatorBase):
    def __init__(self):
        self.__rm = pyvisa.ResourceManager()

    @staticmethod
    def create(addr: str):
        c = CommunicatorVisa()
        c.connect(addr)
        return c

    def connect(self, address: str):
        self.__visa = self.__rm.open_resource(address)
        self.__visa.timeout = 3600000
    def disconnect(self):
        if CommunicatorBase._verbose:
            print("Diconnecting comunicator to {0}".format(self.__address))

        self.__visa.close()

    def send(self, msg: str):
        if CommunicatorBase._verbose:
            print("Sending \"{0}\"".format(msg))

        self.__visa.write((msg + "\n"))

    def read_line(self):
        return self.__visa.read()

