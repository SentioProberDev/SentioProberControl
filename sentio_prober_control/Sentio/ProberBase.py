""" This pakcage contains an abstrach base class for the probe station and a custom exception class for signalling errors.
    @private
"""
from abc import ABC, abstractmethod


class ProberException(Exception):
    """ A custom exception class for SENTIO's python package.

        All errors that occur in this package will be wrapped in this exception class. 
    """

    def __init__(self, msg, errc = -1):
        """ Creates a new ProberException object.
            :param msg: The error message.
            :param errc: The error code (optional). If no error code is set -1 is used.
        """
        super().__init__(msg)
        self.__message = msg
        self.__error = errc


    def error(self):
        """  Get error code. 
            :return: The error code of the exception.
        """
        return self.__error


    def message(self):
        """ Returns the error message.
            :return: The error message.
        """
        return self.__message
    

class ProberBase(ABC):
    """ Abstract base class of a probe station.
        @private
    """
    def __init__(self, comm):
        """ Creates a new ProberBase object.
            :param comm: The communication object used to communicate with the probe station.
        """

        self.comm = comm
        """ The communication object used to communicate with the probe station. """

    @abstractmethod
    def name(self):
        """ Returns the name of the probe station.

            Must be implemented by derived classes.

            :return: The name of the probe station.
        """
        pass

