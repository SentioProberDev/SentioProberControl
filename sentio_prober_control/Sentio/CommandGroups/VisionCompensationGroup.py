from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class VisionCompensationGroup(CommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm)

    def start_execute(self, type: CompensationType, mode: CompensationMode):
        self._comm.send(f'vis:compensation:start_execute {type.toSentioAbbr()}, {mode.toSentioAbbr()}')
        return Response.check_resp(self._comm.read_line())

