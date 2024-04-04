from deprecated import deprecated

from sentio_prober_control.Sentio.Enumerations import ExecuteAction
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


@deprecated("Use VisionCompensationGroup instead")
class WafermapCompensationCommandGroup(CommandGroupBase):

    @deprecated("Use vis.compensation.start_execute(CompensationType.Topography, CompensationMode.Vertical) instead")
    def topography(self, execute: ExecuteAction):
        self.comm.send(f"map:compensation:topography {execute.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())

        # i.e. Stepping while at the end of the route
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.cmd_id()
