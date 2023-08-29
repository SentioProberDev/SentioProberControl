from abc import ABC


class ProberBase(ABC):
    """ Abstract base class of a probe station. """
    def __init__(self, comm):
        self.comm = comm

    def name(self):
        raise NotImplementedError("ProberBase.name is not implemented!")

    def connect(self):
        raise NotImplementedError("ProberBase.connect is not implemented!")


class ProberException(Exception):
    """ A custom exception class for the prober. """
    def __init__(self, msg, errc = -1):
        super().__init__(msg)
        self.__message = msg
        self.__error = errc

    def error(self):
        return self.__error

    def message(self):
        return self.__message


