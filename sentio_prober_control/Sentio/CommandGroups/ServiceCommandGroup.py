from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *


class ServiceCommandGroup(ModuleCommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm, 'service')

    def set_compensation_mode(self, status: bool):
        self._comm.send("service:chuck_compensation {0}".format(status))
        Response.check_resp(self._comm.read_line())

    def set_software_fence(self, fence: SoftwareFence):
        self._comm.send("service:chuck_fence {0}".format(fence.toSentioArg()))
        Response.check_resp(self._comm.read_line())