from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class SiPHCommandGroup(CommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm)

    def move_hover(self, probe: ProbeSentio) -> str:
        self._comm.send("siph:move_hover {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def move_separation(self, probe: ProbeSentio) -> str:
        self._comm.send("siph:move_separation {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def fast_alignment(self) -> str:
        self._comm.send("siph:fast_alignment")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def gradient_search(self) -> str:
        self._comm.send("siph:gradient_search")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def get_intensity(self) -> int:
        self._comm.send("siph:get_intensity")
        resp = Response.check_resp(self._comm.read_line())
        return int(resp.message())

    def get_cap_sensor(self) -> int:
        self._comm.send("siph:get_cap_sensor")
        resp = Response.check_resp(self._comm.read_line())
        return int(resp.message())