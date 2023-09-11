from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *


class VisionCompensationGroup(CommandGroupBase):
    """ This command group contains functions for working with x,y and z compensation. """

    def __init__(self, comm):
        """ @private """
        super().__init__(comm)


    def set_compensation(self, comp:CompensationMode, enable:bool):
        """ Enable or disable compensation for a given subsystem. 

            Wraps Sentios "vis:compensation:enable" command.

            :param comp: The compensation to enable or disable.
            :param enable: True to enable, False to disable.
            :returns: A tuple with the current state of the compensation and the current mode.
        """

        self._comm.send(f"vis:compensation:enable {comp.toSentioAbbr()}, {enable}")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return tok[0], tok[1]


    def start_execute(self, type: CompensationType, mode: CompensationMode):
        """ Start the execution of a compensation.

            Wraps Sentios "vis:compensation:start_execute" remote command.

            :param  type: The type of compensation to execute.
            :param  mode: The mode of compensation to execute.
            :raises: ProberException if an error occured.
            :returns: A Response object.
        """

        self._comm.send(f'vis:compensation:start_execute {type.toSentioAbbr()}, {mode.toSentioAbbr()}')
        return Response.check_resp(self._comm.read_line())

