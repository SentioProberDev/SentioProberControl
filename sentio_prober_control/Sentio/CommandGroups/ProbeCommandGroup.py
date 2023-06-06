from typing import Tuple
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class ProbeCommandGroup(CommandGroupBase):
    __comm = None

    def __init__(self, comm):
        self.__comm = comm

    def move_probe_xy(self, probe: ProbeSentio, ref: ProbeXYReference, x: float, y: float) -> Tuple[float, float]:
        self.__comm.send("move_positioner_xy {0},{1},{2},{3}".format(probe.toSentioAbbr(), ref.toSentioAbbr(), x, y))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def move_probe_z(self, probe: ProbeSentio, ref: ProbeZReference, z: float) -> float:
        self.__comm.send("move_positioner_z {0}, {1}, {2}".format(probe.toSentioAbbr(), ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.__comm.read_line())
        return float(resp.message())

    def get_probe_xy(self, probe: ProbeSentio, ref: ProbeXYReference) -> Tuple[float, float]:
        self.__comm.send("get_positioner_xy {0},{1}".format(probe.toSentioAbbr(), ref.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def get_probe_z(self, probe: ProbeSentio, ref: ProbeZReference) -> float:
        self.__comm.send("get_positioner_z {0}, {1}".format(probe.toSentioAbbr(), ref.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return float(resp.message())

    def set_probe_home(self, probe: ProbeSentio, site: ChuckSite = None, x: float = None, y: float = None) -> float:
        if site == None:
            self.__comm.send("set_positioner_home {0}".format(probe.toSentioAbbr()))
        else:
            self.__comm.send(
                "set_positioner_home {0},{1},{2},{3}".format(probe.toSentioAbbr(), site.toSentioAbbr(), x, y))
        resp = Response.check_resp(self.__comm.read_line())
        return resp.message()

    def move_probe_home(self, probe: ProbeSentio) -> Tuple[float, float]:
        self.__comm.send("move_positioner_home {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def set_probe_contact(self, probe: ProbeSentio, z: float = None) -> float:
        if z == None:
            self.__comm.send("set_positioner_contact {0}".format(probe.toSentioAbbr()))
        else:
            self.__comm.send("set_positioner_contact {0},{1}".format(probe.toSentioAbbr(), z))
        resp = Response.check_resp(self.__comm.read_line())
        return resp.message()

    def move_probe_contact(self, probe: ProbeSentio) -> float:
        self.__comm.send("move_positioner_contact {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return float(resp.message())

    def get_probe_site(self, probe: ProbeSentio, idx: int ) -> int:
        self.__comm.send("get_positioner_site {0},{1}".format(probe.toSentioAbbr(), idx))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")

        return int(tok[0]), str(tok[1]), float(tok[2]), float(tok[3])

    def get_probe_site_number(self, probe: ProbeSentio) -> int:
        self.__comm.send("get_positioner_site_num {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return int(resp.message())

    def step_probe_site(self, probe: ProbeSentio, idx: int )  -> float:
        self.__comm.send("step_positioner_site {0},{1}".format(probe.toSentioAbbr(), idx))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])

    def step_probe_site_first(self, probe: ProbeSentio)  -> float:
        self.__comm.send("step_positioner_site_first {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])

    def step_probe_site_next(self, probe: ProbeSentio)  -> float:
        self.__comm.send("step_positioner_site_next {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])

    def remove_probe_site(self, probe: ProbeSentio, idx: int )  -> float:
        self.__comm.send("remove_positioner_site {0},{1}".format(probe.toSentioAbbr(), idx))
        resp = Response.check_resp(self.__comm.read_line())
        return resp.message()

    def reset_probe_site(self, probe: ProbeSentio)  -> float:
        self.__comm.send("reset_positioner_sites {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return resp.message()

    def async_step_probe_site(self, probe: ProbeSentio, idx: int )  -> float:
        self.__comm.send("start_step_positioner_site {0},{1}".format(probe.toSentioAbbr(), idx))
        resp = Response.check_resp(self.__comm.read_line())
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.cmd_id()

    def async_step_probe_site_next(self, probe: ProbeSentio)  -> float:
        self.__comm.send("start_step_positioner_site_next {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.cmd_id()

    def async_step_probe_site_first(self, probe: ProbeSentio)  -> float:
        self.__comm.send("start_step_positioner_site_first {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.cmd_id()