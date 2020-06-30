from typing import Tuple

from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase
from sentio_prober_control.Sentio.Response import *


class StatusCommandGroup(ModuleCommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm, 'status')

    def get_machine_status(self) -> Tuple[bool, bool, bool]:
        self._comm.send("status:get_machine_status")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        isInitialized = "Ready" in tok
        isMeasuring = "IsMeasuring" in tok
        LoaderBusy = "LoaderBusy" in tok
        return isInitialized, isMeasuring, LoaderBusy

