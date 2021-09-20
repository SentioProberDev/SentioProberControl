from sentio_prober_control.Sentio.Enumerations import *
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.ProberBase import ProberException

from typing import Tuple

class WafermapSubsiteGroup(CommandGroupBase):
    def __init__(self, comm, wafermap_command_group):
        super().__init__(comm)
        self._parent_command_group = wafermap_command_group

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

    def step_next(self):
        self._comm.send('map:subsite:step_next')

        resp = Response.check_resp(self._comm.read_line())
        self._parent_command_group.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute

        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])

    def bin_step_next(self, bin : int):
        self._comm.send(f'map:subsite:bin_step_next {bin}')

        resp = Response.check_resp(self._comm.read_line())
        self._parent_command_group.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute

        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])