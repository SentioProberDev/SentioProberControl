import os
import re
import unittest
from typing import Callable, cast
from unittest.mock import MagicMock, call

from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.CommandGroups.QAlibriaCommandGroup import (
    QAlibriaCommandGroup,
    DriftType,
)
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.Response import Response


# ---------------------------------------------------------------------------
#  Test helpers: DummyResponse and fake_check_resp
# ---------------------------------------------------------------------------

class DummyResponse(Response):
    """
    Minimal replacement for Response used only in unit tests.
    """

    def __init__(self, raw: str) -> None:
        # Expected raw format: "<code>,<id>,<message>"
        parts = raw.split(",", 2)
        self.code: int = int(parts[0]) if parts and parts[0].isdigit() else -1
        self._message: str = parts[2] if len(parts) > 2 else ""

    def message(self) -> str:
        return self._message


def fake_check_resp(raw: str) -> Response:
    """
    Replacement for Response.check_resp used during tests.
    * Returns a Response (DummyResponse) when code == 0.
    * Raises ProberException when code != 0.
    """
    resp: DummyResponse = DummyResponse(raw)
    if resp.code != 0:
        raise ProberException(resp.message(), resp.code)
    return resp


typed_fake: Callable[[str], Response] = cast(Callable[[str], Response], fake_check_resp)
setattr(Response, "check_resp", staticmethod(typed_fake))  # type: ignore[method-assign]

# ---------------------------------------------------------------------------
#  Unit-tests for QAlibriaCommandGroup
# ---------------------------------------------------------------------------

class TestQAlibriaCommandGroup(unittest.TestCase):
    def setUp(self) -> None:
        # Create a mock communicator.
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        # QAlibriaCommandGroup expects a parent object with a 'comm' attribute.
        parent = type("Parent", (), {"comm": self.mock_comm})()
        self.qal = QAlibriaCommandGroup(parent)

    # ------------- basic commands -------------

    def test_calibration_execute(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.calibration_execute()
        self.mock_comm.send.assert_called_with("qal:calibration_execute")

    def test_calibration_drift_verify(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.calibration_drift_verify("DUT1", True)
        self.mock_comm.send.assert_called_with("qal:calibration_drift_verify DUT1,true")

    # ------------- deprecated wrappers -------------

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
        self.mock_comm.read_line.side_effect = [
            "0,0,FirstResponse",
            "0,0,SecondResponse",
        ]
        result = self.qal.set_calibration_drift_probe12()
        self.assertEqual(result, "SecondResponse")
        self.mock_comm.send.assert_has_calls(
            [
                call("qal:set_dut_network RefDUT,DriftRef,12,false"),
                call("qal:set_dut_network RefDUT,Drift,12,false"),
            ]
        )

    # ------------- new commands -------------

    def test_check_calibration_status_ok(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.qal.check_calibration_status()
        self.mock_comm.send.assert_called_with("qal:get_calibration_status")
        self.assertIsNone(result)

    def test_check_calibration_status_error(self):
        self.mock_comm.read_line.return_value = (
            "451,0,Substrate not setup at 'Wafer' site"
        )
        with self.assertRaises(ProberException):
            self.qal.check_calibration_status()

    def test_measurement_execute(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.measurement_execute("test.snp", [1, 2], True, False, True)
        self.mock_comm.send.assert_called_with(
            "qal:measurement_execute test.snp,1,2,true,false,true"
        )

    def test_reset_ets(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.reset_ets()
        self.mock_comm.send.assert_called_with("qal:reset_ets")

    def test_set_ets(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        path = os.path.join("D:", "temp", "ets.txt")
        self.qal.set_ets(12, path)
        expected = rf"qal:set_ets 12,{re.escape(path)},0"
        self.assertRegex(self.mock_comm.send.call_args.args[0], expected)

    def test_send_ets_to_vna(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.send_ets_to_vna("cal_set_p12")
        self.mock_comm.send.assert_called_with("qal:send_ets_to_vna cal_set_p12")

    def test_clear_dut_network(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.clear_dut_network("RefDUT", DriftType.DriftRef, True)
        self.mock_comm.send.assert_called_with(
            "qal:clear_dut_network RefDUT,DriftRef,true"
        )

    def test_vna_write(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.qal.vna_write(":SENS1:FREQ:STAR 1.0E9")
        self.mock_comm.send.assert_called_with(
            "qal:vna_write :SENS1:FREQ:STAR 1.0E9"
        )

    def test_vna_query(self):
        self.mock_comm.read_line.return_value = "0,0,1.0E9"
        result = self.qal.vna_query(":SENS1:FREQ:STAR?")
        self.mock_comm.send.assert_called_with(
            "qal:vna_query :SENS1:FREQ:STAR?"
        )
        self.assertEqual(result, "1.0E9")

    def test_vna_read(self):
        self.mock_comm.read_line.return_value = "0,0,Data"
        result = self.qal.vna_read()
        self.mock_comm.send.assert_called_with("qal:vna_read")
        self.assertEqual(result, "Data")


if __name__ == "__main__":
    unittest.main()
