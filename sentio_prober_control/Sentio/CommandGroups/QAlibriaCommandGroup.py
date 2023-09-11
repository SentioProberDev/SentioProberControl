from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class QAlibriaCommandGroup(CommandGroupBase):
    """ This command group contains functions for working with Qalibria. """
    
    def __init__(self, comm):
        """ @private """
        super().__init__(comm)


    # Inconsistent API filed as CR#13887. This function should not exist!
    # the use of the "start_" prefix implies it is an async function. It is not or 
    # if it is where it the command id return value?
    def start_calibration(self) -> None:
        """ @private """
        self._comm.send("qal:calibration_execute")
        Response.check_resp(self._comm.read_line())


    # Inconsistent API filed as CR#13887. This function should not exist!
    def verify_calibration_drift(self) -> None:
        """ @private """        
        self._comm.send("qal:calibration_drift_verify")
        Response.check_resp(self._comm.read_line())


    # Inconsistent API filed as CR#13887. This function should not exist!
    def verify_calibration_drift_dut(self, dut) -> None:
        """ @private """
        self._comm.send("qal:calibration_drift_verify {}".format(dut))
        Response.check_resp(self._comm.read_line())


    # Inconsistent API filed as CR#13887. This function should not exist!
    def set_calibration_drift_probe12(self):
        """ @private """                
        self._comm.send(" qal:set_dut_network RefDUT,DriftRef,12,false")
        resp = Response.check_resp(self._comm.read_line())

        self._comm.send(" qal:set_dut_network RefDUT,Drift,12,false")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()