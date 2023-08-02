from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class QAlibriaCommandGroup(CommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm)

    def start_calibration(self):
        self._comm.send("qal:calibration_execute")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def verify_calibration_drift(self):
        self._comm.send("qal:calibration_drift_verify")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def verify_calibration_drift_dut(self, dut):
        self._comm.send("qal:calibration_drift_verify {}".format(dut))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def set_calibration_drift_probe12(self):
        self._comm.send(" qal:set_dut_network RefDUT,DriftRef,12,false")
        resp = Response.check_resp(self._comm.read_line())
        self._comm.send(" qal:set_dut_network RefDUT,Drift,12,false")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()