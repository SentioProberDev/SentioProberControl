from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *

from sentio_prober_control.Sentio.ProberBase import ProberException

@deprecated("Use VisionCompensationGroup instead")
class WafermapCompensationCommandGroup(CommandGroupBase):
    """ This command group bundles functions for setting up and using position compensation. 

        .. deprecated:: 23.2 Use VisionCompensationGroup instead

        @private
    """

    @deprecated("Use vis.compensation.start_execute(CompensationType.Topography, CompensationMode.Vertical) instead")
    def topography(self, execute : ExecuteAction):
        """ Execute the topography compensation. This is an asynchronous command.

             .. deprecated:: 23.2 Use vis.compensation.start_execute(CompensationType.Topography, CompensationMode.Vertical) instead

            Topography compensation is a height scan of the wafer based on focus height variations.

            Wraps SENTIO's map:compensation:topography remote command.

            :param execute: Specifes what to do. Execute or abort the compensation.
            :raises ProberException: if the command could not be executed successfully.
            :returns: The async command id of the command.

            @private            
        """
        self._comm.send(f"map:compensation:topography {execute.toSentioAbbr()}")
        resp = Response.check_resp(self._comm.read_line())

        # i.e. Stepping while at the end of the route
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.cmd_id()
