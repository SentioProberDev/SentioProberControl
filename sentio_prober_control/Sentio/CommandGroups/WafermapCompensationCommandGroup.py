from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *

from sentio_prober_control.Sentio.ProberBase import ProberException

class WafermapCompensationCommandGroup(CommandGroupBase):
    def topography(self, execute : ExecuteAction):
        self._comm.send("map:compensation:topography {}".format(execute.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())

        # i.e. Stepping while at the end of the route
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.cmd_id()
