from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *
from sentio_prober_control.Sentio.CommandGroups.AuxCleaningGroup import  AuxCleaningGroup
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase

class AuxCommandGroup(ModuleCommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm, 'aux')

        self.cleaning = AuxCleaningGroup(comm)

    def start_clean(self):
        self._comm.send("aux:cleaning:start")
        resp = Response.check_resp(self._comm.read_line())
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.message()

