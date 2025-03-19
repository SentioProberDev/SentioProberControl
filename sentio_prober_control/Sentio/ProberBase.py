from abc import ABC, abstractmethod

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase


class ProberException(Exception):
    """A custom exception class for SENTIO's python package.

    All errors that occur in this package will be wrapped in this exception class.
    """

    def __init__(self, msg: str, errc: int = -1):
        """Create a new ProberException object.

        Args:
            msg (str): The error message.
            errc (int): The error code (optional). If no error code is set -1 is used.
        """
        super().__init__(msg)
        self.__message = msg
        self.__error = errc

    def error(self):
        """Get error code.

        Returns:
            errc (int): The error code of the exception.
        """
        return self.__error

    def message(self):
        """Returns the error message.

        Returns:
            errorcode (str): The error message.
        """
        return self.__message


class ProberBase(ABC):
    """Abstract base class of a probe station."""

    def __init__(self, comm: CommunicatorBase):
        """Creates a new ProberBase object.

        Attributes:
            comm (CommunicatorBase): The communication object used to communicate with the probe station.

        Args:
            comm (CommunicatorBase): The communication object used to communicate with the probe station.
        """

        self.__comm = comm


    @property
    def comm(self) -> CommunicatorBase:
        """Get the communicator object.

        Returns:
            comm (CommunicatorBase): The communicator object.
        """
        return self.__comm
    

    @abstractmethod
    def name(self) -> str:
        """Returns the name of the probe station.

        Must be implemented by derived classes.

        Returns:
            name (str): The name of the probe station.
        """
        pass
