from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *

from sentio_prober_control.Sentio.ProberBase import ProberException

class WafermapDieCommandGroup(CommandGroupBase):
    def remove(self, x: int, y: int):
        self._comm.send("map:die:remove {0}, {1}".format(x, y))
        Response.check_resp(self._comm.read_line())
