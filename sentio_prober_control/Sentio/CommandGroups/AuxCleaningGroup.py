from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *


class AuxCleaningGroup(CommandGroupBase):
    """ Command group for cleaning the probe. """

    def enable_auto(self, stat:bool):
        """ Enable automatic probe cleaning.

            :param stat: A flag indicating whether to enable or disable cleaning. 
            :raises: ProberException if the response indicates an error.
        """
        self._comm.send("aux:cleaning:enable_auto {0}".format(stat))
        Response.check_resp(self._comm.read_line())

    def start(self, touchdowns:int):
        """ Start the cleaning procedure. 
        
            :param touchdowns: The number of touchdowns to perform.
            :raises: ProberException if the response indicates an error.
        """
        self._comm.send("aux:cleaning:start {0}".format(touchdowns))
        Response.check_resp(self._comm.read_line())
