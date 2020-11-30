from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *


class WafermapPoiCommandGroup(CommandGroupBase):

    def reset(self, stage : Stage, refXy : PoiReferenceXy):
        self._comm.send("map:poi:reset {0}, {1}".format(stage.toSentioAbbr(), refXy.toSentioAbbr()))
        Response.check_resp(self._comm.read_line())

    def add(self, x, y, desc):
        self._comm.send("map:poi:add {0}, {1}, {2}".format(x, y, desc))
        Response.check_resp(self._comm.read_line())

    def get_num(self):
        self._comm.send("map:poi:get_num")
        resp = Response.check_resp(self._comm.read_line())
        return int(resp.message())

    def step(self, target):
        self._comm.send("map:poi:step {0}".format(target))
        Response.check_resp(self._comm.read_line())

    def step_first(self):
        self._comm.send("map:poi:step_first")
        Response.check_resp(self._comm.read_line())

    def step_next(self):
        self._comm.send("map:poi:step_next")
        Response.check_resp(self._comm.read_line())

