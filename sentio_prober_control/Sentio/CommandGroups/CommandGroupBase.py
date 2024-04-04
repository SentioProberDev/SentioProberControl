from abc import ABC
from typing import Union

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase


class CommandGroupBase(ABC):
    """Base class for all command groups.

    The functionality of the prober control suiote is organized in command groups.
    Each command group contains a set of commands that are logically related.
    """

    def __init__(self, parent : Union['CommandGroupBase', 'SentioProber']) -> None:
        self.__parent = parent


    @property
    def prober(self) -> 'SentioProber':
        """Get the prober object.

        Returns:
            prober (SentioProber): The prober object.
        """

        from sentio_prober_control.Sentio.ProberSentio import SentioProber

        if isinstance(self.__parent, SentioProber):
            return self.__parent
        else:
            return self.__parent.prober
        
       
    @property
    def comm(self) -> CommunicatorBase:
        """Get the communicator object.

        Returns:
            comm (CommunicatorBase): The communicator object.
        """
        return self.__parent.comm
