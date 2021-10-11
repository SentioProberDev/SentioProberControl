from abc import ABC


class CommunicatorBase(ABC):
    _verbose = False

    def connect(self):
        raise NotImplementedError("CommunicatorBase.connect is not implemented!")

    def disconnect(self):
        raise NotImplementedError("CommunicatorBase.disconnect is not implemented!")

    def send(self, msg: str):
        raise NotImplementedError("CommunicatorBase.send is not implemented!")

    def read_line(self):
        raise NotImplementedError("CommunicatorBase.read_line is not implemented!")

