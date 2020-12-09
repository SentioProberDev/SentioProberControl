from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *


class AuxCleaningGroup(CommandGroupBase):
    def enable_auto(self, stat:bool):
        self._comm.send("aux:cleaning:enable_auto {0}".format(stat))
        Response.check_resp(self._comm.read_line())

    def start(self, touchdowns:int):
        self._comm.send("aux:cleaning:start {0}".format(touchdowns))
        Response.check_resp(self._comm.read_line())
