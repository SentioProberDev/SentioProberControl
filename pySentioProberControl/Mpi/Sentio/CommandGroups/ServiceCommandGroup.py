from Mpi.Sentio.CommandGroups.CommandGroupBase import *
from Mpi.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase
from Mpi.Sentio.Response import *
from Mpi.Sentio.Enumerations import *


class ServiceCommandGroup(ModuleCommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm, 'service')

    def set_compensation_mode(self, status:bool):
        self._comm.send("service:chuck_compensation {0}".format(status))
        Response.check_resp(self._comm.read_line())

    def set_software_fence(self, fence: SoftwareFence):
        self._comm.send("service:chuck_fence {0}".format(fence.toSentioArg()))
        Response.check_resp(self._comm.read_line())