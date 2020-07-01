from sentio_prober_control.Sentio.Enumerations import AxisOrient
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase

from typing import Tuple

class WafermapSubsiteGroup(CommandGroupBase):
    def get_num(self) -> int:
        self._comm.send("map:subsite:get_num")
        resp = Response.check_resp(self._comm.read_line())
        return int(resp.message())

    def get(self, idx) -> Tuple[str, float, float]:
        self._comm.send("map:subsite:get {0}".format(idx))
        resp = Response.check_resp(self._comm.read_line())

        tok = resp.message().split(",")
        return str(tok[0]), float(tok[1]), float(tok[2])

    """ Reset Sentios subsite definitions. """
    def reset(self):
        self._comm.send("map:subsite:reset")
        Response.check_resp(self._comm.read_line())

    """ Add a single subsite to the wafermap """
    def add(self, id: str, x: float, y: float, orient: AxisOrient = AxisOrient.UpRight):
        self._comm.send("map:subsite:add {}, {}, {}, {}".format(id, x, y, orient.toSentioAbbr()))
        Response.check_resp(self._comm.read_line())
