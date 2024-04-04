from deprecated import deprecated

from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class QAlibriaCommandGroup(CommandGroupBase):
    """This command group contains functions for working with Qalibria."""

    def __init__(self, comm) -> None:
        super().__init__(comm)


    def calibration_execute(self) -> None:
        """Execute VNA calibration.

        Wraps SENTIO's "qal:calibration_execute" remote command.
        """
        self.comm.send("qal:calibration_execute")
        Response.check_resp(self.comm.read_line())


    def calibration_drift_verify(self, dut_name: str = "", auto_exec: bool = True) -> None:
        """Calibration Drift verification.

        Wraps SENTIO's "qal:calibration_drift_verify" remote command.

        Args:
            dut_name: The name of the dut.
            auto_exec:
        """
        self.comm.send("qal:calibration_drift_verify {dut_name}, {auto_exec}")
        resp = Response.check_resp(self.comm.read_line())

    # Inconsistent API filed as CR#13887. This function should not exist!
    # the use of the "start_" prefix implies it is an async function. It is not or
    # if it is where it the command id return value?
    @deprecated(reason="use calibration_execute instead!; this function violates naming conventions since its name is different from the remote command; filed as CR#13887")
    def start_calibration(self) -> None:
        self.comm.send("qal:calibration_execute")
        Response.check_resp(self.comm.read_line())


    # Inconsistent API filed as CR#13887. This function should not exist!
    @deprecated(reason="use calibration_drift_verify instead!; this function violates naming conventions since its name is different from the remote command; filed as CR#13887")
    def verify_calibration_drift(self) -> None:
        self.comm.send("qal:calibration_drift_verify")
        Response.check_resp(self.comm.read_line())


    # Inconsistent API filed as CR#13887. This function should not exist!
    @deprecated(reason="use calibration_drift_verify instead!; this function violates naming conventions since its name is different from the remote command; filed as CR#13887")
    def verify_calibration_drift_dut(self, dut) -> None:
        self.comm.send("qal:calibration_drift_verify {}".format(dut))
        Response.check_resp(self.comm.read_line())


    # Inconsistent API filed as CR#13887. This function should not exist!
    @deprecated(reason="oddly specific function name; filed as CR#13887")
    def set_calibration_drift_probe12(self):
        self.comm.send(" qal:set_dut_network RefDUT,DriftRef,12,false")
        resp = Response.check_resp(self.comm.read_line())

        self.comm.send(" qal:set_dut_network RefDUT,Drift,12,false")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
