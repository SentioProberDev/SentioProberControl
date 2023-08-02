from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *
from typing import Tuple

class VisionCameraCommandGroup(CommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm)

    def set_light(self, mp: CameraMountPoint, value: int):
        self._comm.send("vis:set_prop light, {0}, {1}".format(mp.toSentioAbbr(), value))
        Response.check_resp(self._comm.read_line())

    def set_exposure(self, mp: CameraMountPoint, value: int):
        self._comm.send("vis:set_prop exposure, {0}, {1}".format(mp.toSentioAbbr(), value))
        Response.check_resp(self._comm.read_line())

    def set_gain(self, mp: CameraMountPoint, value: float):
        self._comm.send("vis:set_prop gain, {0}, {1}".format(mp.toSentioAbbr(), value))
        Response.check_resp(self._comm.read_line())

    def get_light(self, mp: CameraMountPoint) -> int:
        self._comm.send("vis:get_prop light, {0}".format(mp.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return int(resp.message())

    def get_exposure(self, mp: CameraMountPoint) -> int:
        self._comm.send("vis:get_prop exposure, {0}".format(mp.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return int(resp.message())

    def get_focus_value(self, mp: CameraMountPoint, alg: AutoFocusAlgorithm):
        self._comm.send("vis:get_focus_value {0}, {1}".format(mp.toSentioAbbr(), alg.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return float(resp.message())

    def get_gain(self, mp: CameraMountPoint) -> float:
        self._comm.send("vis:get_prop gain, {0}".format(mp.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return float(resp.message())

    def get_calib(self, mp: CameraMountPoint) -> Tuple[float, float]:
        self._comm.send("vis:get_prop calib, {0}".format(mp.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def get_image_size(self, mp: CameraMountPoint) -> Tuple[int, int]:
        self._comm.send("vis:get_prop image_size, {0}".format(mp.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1])

    def is_pattern_trained(self, mp: CameraMountPoint, pat: any) -> bool:
        if isinstance(pat, DefaultPattern):
            pattern_name = pat.toSentioAbbr()
        else:
            pattern_name = pat

        self._comm.send("vis:pattern:is_trained {}, {}".format(mp.toSentioAbbr(), pattern_name))
        resp = Response.check_resp(self._comm.read_line())
        is_trained = resp.message() == '1'
        return is_trained

#    def is_pattern_trained(self, mp: CameraMountPoint, pat: DefaultPattern) -> bool:
#        self._comm.send("vis:pattern:is_trained {}, {}".format(mp.toSentioAbbr(), pat.toSentioAbbr()))
#        resp = Response.check_resp(self._comm.read_line())
#        is_trained = resp.message() == '1'
#        return is_trained
