from abc import ABC

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase

class CommandGroupBase(ABC):
    """ Base class for all command groups.
     
        The functionality of the prober control suiote is organized in command groups.
        Each command group contains a set of commands that are logically related.
    """
    def __init__(self, comm : CommunicatorBase):
        self._comm = comm
