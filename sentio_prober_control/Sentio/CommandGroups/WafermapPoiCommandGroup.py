from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *


class WafermapPoiCommandGroup(CommandGroupBase):

    def reset(self):
        self._comm.send("map:poi:reset chuck, diecenter")
        Response.check_resp(self._comm.read_line())

    def add(self, x, y, desc):
        #
        self._comm.send("map:poi:add {0}, {1}, {2}")
        Response.check_resp(self._comm.read_line())
