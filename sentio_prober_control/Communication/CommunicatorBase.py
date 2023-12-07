from abc import ABC


class CommunicatorBase(ABC):
    """Base class for all communicators.

    Communicators ore objects that implement different communication protocols
    for talking to the probe station.
    """

    _verbose = False

    def connect(self):
        """Connect to the probe station.

        Must be implemented by the derived class.
        """
        raise NotImplementedError("CommunicatorBase.connect is not implemented!")

    def disconnect(self):
        """Disconnect from the probe station.

        Must be implemented by the derived class.
        """
        raise NotImplementedError("CommunicatorBase.disconnect is not implemented!")

    def send(self, msg: str):
        """Send a command to the probe station.

        Must be implemented by the derived class.
        """
        raise NotImplementedError("CommunicatorBase.send is not implemented!")

    def read_line(self):
        """Read a line from the probe station.

        Must be implemented by the derived class.
        """
        raise NotImplementedError("CommunicatorBase.read_line is not implemented!")
