import unittest
from unittest.mock import MagicMock, call
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.CommandGroups.QAlibriaCommandGroup import QAlibriaCommandGroup, DriftType
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.ProberBase import ProberException

# Dummy response class to simulate Response objects from check_resp.
class DummyResponse:
    def __init__(self, resp_str):
        # Expected format: "error_code,command_id,message"
        parts = resp_str.split(",")
        if len(parts) >= 3:
            self._message = parts[2]
        elif len(parts) == 2:
            self._message = parts[1]
        else:
            self._message = ""
    def message(self):
        return self._message

# Patch Response.check_resp to return a DummyResponse instance.
Response.check_resp = lambda x: DummyResponse(x)

# Dummy parent class that contains a 'comm' attribute.
class DummyParent:
    def __init__(self, comm):
        self.comm = comm

class TestQAlibriaCommandGroup(unittest.TestCase):
    def setUp(self):
        # Create a mock communicator based on the TCP/IP communicator.
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        # Wrap the communicator in a dummy parent so that __parent.comm works.
        dummy_parent = DummyParent(self.mock_comm)
        self.qal = QAlibriaCommandGroup(dummy_parent)

    def test_calibration_execute(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.calibration_execute()
        self.mock_comm.send.assert_called_with("qal:calibration_execute")

    def test_calibration_drift_verify(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.calibration_drift_verify("DUT1", True)
        self.mock_comm.send.assert_called_with("qal:calibration_drift_verify DUT1,true")

    def test_start_calibration_deprecated(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.start_calibration()
        self.mock_comm.send.assert_called_with("qal:calibration_execute")

    def test_verify_calibration_drift_deprecated(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.verify_calibration_drift()
        self.mock_comm.send.assert_called_with("qal:calibration_drift_verify")

    def test_verify_calibration_drift_dut_deprecated(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.verify_calibration_drift_dut("DUT2")
        self.mock_comm.send.assert_called_with("qal:calibration_drift_verify DUT2")

    def test_set_calibration_drift_probe12_deprecated(self):
        # Provide two responses for the two sequential send commands.
        self.mock_comm.read_line.side_effect = ["0,0,FirstResponse", "0,0,SecondResponse"]
        result = self.qal.set_calibration_drift_probe12()
        expected_calls = [
            call("qal:set_dut_network RefDUT,DriftRef,12,false"),
            call("qal:set_dut_network RefDUT,Drift,12,false")
        ]
        self.mock_comm.send.assert_has_calls(expected_calls)
        self.assertEqual(result, "SecondResponse")

    def test_check_calibration_status_ok(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        # check_calibration_status should not return any value and not raise an exception.
        result = self.qal.check_calibration_status()
        self.mock_comm.send.assert_called_with("qal:get_calibration_status")
        self.assertIsNone(result)

    def test_check_calibration_status_error(self):
        self.mock_comm.read_line.return_value = "0,0,ERROR"
        with self.assertRaises(ProberException):
            self.qal.check_calibration_status()

    def test_measurement_execute(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        # Now use ports as a list of integers.
        self.qal.measurement_execute("test.snp", [1, 2], True, False, True)
        expected_cmd = "qal:measurement_execute test.snp,1,2,true,false,true"
        self.mock_comm.send.assert_called_with(expected_cmd)

    def test_reset_ets(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.reset_ets()
        self.mock_comm.send.assert_called_with("qal:reset_ets")

    def test_set_ets(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        # Pass an integer for port.
        self.qal.set_ets(12, "D:\\temp\\ets.txt")
        expected_cmd = "qal:set_ets 12,D:\\temp\\ets.txt,0"
        self.mock_comm.send.assert_called_with(expected_cmd)

    def test_send_ets_to_vna(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.send_ets_to_vna("cal_set_p12")
        expected_cmd = "qal:send_ets_to_vna cal_set_p12"
        self.mock_comm.send.assert_called_with(expected_cmd)

    def test_clear_dut_network(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        # Pass DriftType.DriftRef instead of a string.
        self.qal.clear_dut_network("RefDUT", DriftType.DriftRef, True)
        expected_cmd = "qal:clear_dut_network RefDUT,DriftRef,true"
        self.mock_comm.send.assert_called_with(expected_cmd)

    def test_vna_write(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.vna_write(":SENS1:FREQ:STAR 1.0E9")
        expected_cmd = "qal:vna_write :SENS1:FREQ:STAR 1.0E9"
        self.mock_comm.send.assert_called_with(expected_cmd)

    def test_vna_query(self):
        self.mock_comm.read_line.return_value = "0,0,1.0E9"
        result = self.qal.vna_query(":SENS1:FREQ:STAR?")
        expected_cmd = "qal:vna_query :SENS1:FREQ:STAR?"
        self.mock_comm.send.assert_called_with(expected_cmd)
        self.assertEqual(result, "1.0E9")

    def test_vna_read(self):
        self.mock_comm.read_line.return_value = "0,0,Data"
        result = self.qal.vna_read()
        self.mock_comm.send.assert_called_with("qal:vna_read")
        self.assertEqual(result, "Data")

if __name__ == "__main__":
    unittest.main()
