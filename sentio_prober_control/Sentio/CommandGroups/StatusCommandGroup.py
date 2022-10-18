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

    def get_chuck_temp(self) -> float:
        self._comm.send("status:get_chuck_temp")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        temp = float(tok[0])
        return temp 

    def get_chuck_temp_setpoint(self) -> float:
        self._comm.send("status:get_chuck_temp_setpoint")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        temp = float(tok[0])
        return temp 

    def set_chuck_temp(self, temp:float):
        self._comm.send(f"status:set_chuck_temp {temp:.2f}")
        resp = Response.check_resp(self._comm.read_line())

    def get_chuck_thermo_state(self) -> Tuple[bool, bool, bool, bool, bool, bool]:
        self._comm.send("status:get_chuck_thermo_state")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        isCooling = "Cooling" in tok
        isHeating = "Heating" in tok
        isControlling = "Controlling" in tok
        isStandby = "Standby" in tok
        isError = "Error" in tok
        isUncontrolled = "Uncontrolled" in tok 
        return isCooling, isHeating, isControlling, isStandby, isError, isUncontrolled 


    def get_soaking_time(self, temp:float):
        self._comm.send(f"status:get_soaking_time {temp:.2f}")
        resp = Response.check_resp(self._comm.read_line())
        temp = float(resp.message())
        return temp