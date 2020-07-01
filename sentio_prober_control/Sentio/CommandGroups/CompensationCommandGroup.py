from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *


class CompensationCommandGroup(CommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm)

    def set_compensation(self, comp:Compensation, enable:bool):
        self._comm.send("vis:compensation:enable {},{}".format(comp.toSentioAbbr(), enable))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        print(resp)
        return tok[0], tok[1]

    def execute_compensation(self, comp:ExecuteCompensation, mode:OnTheFlyMode):
        self._comm.send("vis:compensation:start_execute {},{}".format(comp.toSentioAbbr(), mode.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return resp