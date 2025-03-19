from deprecated import deprecated
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase

class QAlibriaCommandGroup(CommandGroupBase):
    """
    This command group contains functions for working with QAlibria.
    """

    def __init__(self, comm) -> None:
        super().__init__(comm)

    def calibration_execute(self) -> None:
        """
        Execute VNA calibration.

        Wraps SENTIO's "qal:calibration_execute" remote command.
        """
        self.comm.send("qal:calibration_execute")
        Response.check_resp(self.comm.read_line())

    def calibration_drift_verify(self, dut_name: str = "", auto_exec: bool = True) -> None:
        """
        Calibration Drift verification.

        Wraps SENTIO's "qal:calibration_drift_verify" remote command.

        Args:
            dut_name: The name of the DUT.
            auto_exec: Whether to automatically execute the drift verify process.
        """
        self.comm.send(f"qal:calibration_drift_verify {dut_name},{str(auto_exec).lower()}")
        Response.check_resp(self.comm.read_line())

    @deprecated(reason="use calibration_execute instead!; violates naming conventions. (CR#13887)")
    def start_calibration(self) -> None:
        """
        Deprecated function for starting calibration.
        Please use calibration_execute instead.
        """
        self.comm.send("qal:calibration_execute")
        Response.check_resp(self.comm.read_line())

    @deprecated(reason="use calibration_drift_verify instead!; violates naming conventions. (CR#13887)")
    def verify_calibration_drift(self) -> None:
        """
        Deprecated function for verifying calibration drift.
        Please use calibration_drift_verify instead.
        """
        self.comm.send("qal:calibration_drift_verify")
        Response.check_resp(self.comm.read_line())

    @deprecated(reason="use calibration_drift_verify instead!; violates naming conventions. (CR#13887)")
    def verify_calibration_drift_dut(self, dut) -> None:
        """
        Deprecated function for verifying calibration drift with a specific DUT.
        Please use calibration_drift_verify(dut_name, ...) instead.
        """
        self.comm.send(f"qal:calibration_drift_verify {dut}")
        Response.check_resp(self.comm.read_line())

    @deprecated(reason="oddly specific function name; filed as CR#13887")
    def set_calibration_drift_probe12(self):
        """
        Deprecated function for setting calibration drift for probe 1 and 2.
        """
        self.comm.send("qal:set_dut_network RefDUT,DriftRef,12,false")
        Response.check_resp(self.comm.read_line())

        self.comm.send("qal:set_dut_network RefDUT,Drift,12,false")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    # -------------------------------------------------------------------------
    # New / Additional Commands
    # -------------------------------------------------------------------------

    def get_calibration_status(self) -> str:
        """
        Retrieve the status of QAlibria.

        Wraps SENTIO's "qal:get_calibration_status" remote command.

        Returns:
            str: The status string of QAlibria (e.g., "OK"). If "OK" and
                 the system is in Remote mode, calibration is ready.
        """
        self.comm.send("qal:get_calibration_status")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def measurement_execute(
        self,
        file_name: str,
        ports: str = "1,2",
        correct_by_vna: bool = True,
        enable_use_ratio: bool = False,
        enable_switch_term: bool = False
    ) -> None:
        """
        Execute a VNA measurement.

        Wraps SENTIO's "qal:measurement_execute" remote command.

        Args:
            file_name: The path to the SNP file.
            ports: The port(s) used for the measurement, e.g. "1,2".
            correct_by_vna: Whether to apply VNA correction (True/False).
            enable_use_ratio: Whether to enable 'Use Ratio b/a' (True/False).
            enable_switch_term: Whether to enable switch term (True/False).
        """
        cmd = (
            f"qal:measurement_execute "
            f"{file_name},{ports},"
            f"{str(correct_by_vna).lower()},"
            f"{str(enable_use_ratio).lower()},"
            f"{str(enable_switch_term).lower()}"
        )
        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def reset_ets(self) -> None:
        """
        Reset error terms in the buffer.

        Wraps SENTIO's "qal:reset_ets" remote command.
        """
        self.comm.send("qal:reset_ets")
        Response.check_resp(self.comm.read_line())

    def set_ets(self, ports: str, path: str) -> None:
        """
        Set error terms in the buffer.

        Wraps SENTIO's "qal:set_ets" remote command.

        Args:
            ports: Port(s) of error terms (e.g. "12").
            path: Path to the error terms file in the buffer (e.g. "D:\\temp\\ets.txt").
        """
        cmd = f"qal:set_ets {ports},{path}"
        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def send_ets_to_vna(self, cal_set_name: str) -> None:
        """
        Send current error terms in QAlibria buffer to the VNA.

        Wraps SENTIO's "qal:send_ets_to_vna" remote command.

        Args:
            cal_set_name: The name of the cal set in the VNA (e.g. "cal_set_p12").
        """
        cmd = f"qal:send_ets_to_vna {cal_set_name}"
        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def clear_dut_network(self, dut_name: str, drift_type: str, update_ui: bool) -> None:
        """
        Clear network data for a DUT.

        Wraps SENTIO's "qal:clear_dut_network" remote command.

        Args:
            dut_name: The name of the DUT (e.g. "RefDUT").
            drift_type: The type of drift data to clear ("DriftRef" or "Drift").
            update_ui: Whether to update the UI (True/False).
        """
        cmd = (
            f"qal:clear_dut_network "
            f"{dut_name},{drift_type},{str(update_ui).lower()}"
        )
        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def vna_write(self, vna_command: str) -> None:
        """
        Write a remote command to the VNA.

        Wraps SENTIO's "qal:vna_write" remote command.

        Args:
            vna_command: The remote command to send to the VNA (e.g. ":SENS1:FREQ:STAR 1.0E9").
        """
        cmd = f"qal:vna_write {vna_command}"
        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def vna_query(self, vna_command: str) -> str:
        """
        Query a remote command from the VNA and return the response.

        Wraps SENTIO's "qal:vna_query" remote command.

        Args:
            vna_command: The remote command to query the VNA (e.g. ":SENS1:FREQ:STAR?").

        Returns:
            str: The response string from the VNA.
        """
        cmd = f"qal:vna_query {vna_command}"
        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def vna_read(self) -> str:
        """
        Read data from the VNA.

        Wraps SENTIO's "qal:vna_read" remote command.

        Returns:
            str: The data in the VNA buffer.
        """
        self.comm.send("qal:vna_read")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()