import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.Enumerations import ThermoChuckState, ChuckThermoEnergyMode, ChuckThermoHoldMode, HighPurgeState
from sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup import StatusCommandGroup
from sentio_prober_control.Sentio.Response import Response

class TestStatusCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock()
        self.mock_parent = MagicMock()
        self.mock_parent.comm = self.mock_comm
        self.cmd = StatusCommandGroup(self.mock_parent)

    def mock_response(self, message="OK"):
        mock_resp = MagicMock()
        mock_resp.message.return_value = message
        return mock_resp

    def test_get_chuck_temp(self):
        self.mock_comm.read_line.return_value = "0,0,25.0"
        Response.check_resp = MagicMock(return_value=self.mock_response("25.0"))
        temp = self.cmd.get_chuck_temp()
        self.assertEqual(temp, 25.0)

    def test_get_chuck_temp_setpoint(self):
        Response.check_resp = MagicMock(return_value=self.mock_response("30.0"))
        temp = self.cmd.get_chuck_temp_setpoint()
        self.assertEqual(temp, 30.0)

    def test_get_chuck_thermo_state(self):
        Response.check_resp = MagicMock(return_value=self.mock_response("cooling"))
        state = self.cmd.get_chuck_thermo_state()
        self.assertEqual(state, ThermoChuckState.Cooling)

    def test_get_machine_status(self):
        Response.check_resp = MagicMock(return_value=self.mock_response("Ready,IsMeasuring,LoaderBusy"))
        result = self.cmd.get_machine_status()
        self.assertEqual(result, (True, True, True))

    def test_get_soaking_time(self):
        Response.check_resp = MagicMock(return_value=self.mock_response("60.0"))
        seconds = self.cmd.get_soaking_time(80.0)
        self.assertEqual(seconds, 60.0)

    def test_get_chuck_thermo_energy_mode(self):
        Response.check_resp = MagicMock(return_value=self.mock_response("Fast"))
        result = self.cmd.get_chuck_thermo_energy_mode()
        self.assertEqual(result, ChuckThermoEnergyMode.Fast)

    def test_set_chuck_thermo_energy_mode_enum(self):
        Response.check_resp = MagicMock(return_value=self.mock_response())
        resp = self.cmd.set_chuck_thermo_energy_mode(ChuckThermoEnergyMode.Optimal)
        self.assertTrue(resp.message(), "OK")

    def test_set_chuck_thermo_energy_mode_str(self):
        Response.check_resp = MagicMock(return_value=self.mock_response())
        resp = self.cmd.set_chuck_thermo_energy_mode("HighPower")
        self.assertTrue(resp.message(), "OK")

    def test_get_chuck_thermo_hold_mode(self):
        Response.check_resp = MagicMock(return_value=self.mock_response("Active"))
        result = self.cmd.get_chuck_thermo_hold_mode()
        self.assertEqual(result, ChuckThermoHoldMode.Active)

    def test_set_chuck_thermo_hold_mode_bool(self):
        Response.check_resp = MagicMock(return_value=self.mock_response())
        resp = self.cmd.set_chuck_thermo_hold_mode(True)
        self.assertTrue(resp.message(), "OK")

    def test_set_chuck_thermo_hold_mode_enum(self):
        Response.check_resp = MagicMock(return_value=self.mock_response())
        resp = self.cmd.set_chuck_thermo_hold_mode(ChuckThermoHoldMode.Nonactive)
        self.assertTrue(resp.message(), "OK")

    def test_get_high_purge_state(self):
        Response.check_resp = MagicMock(return_value=self.mock_response("On"))
        result = self.cmd.get_high_purge_state()
        self.assertEqual(result, HighPurgeState.On)

    def test_set_high_purge_bool(self):
        Response.check_resp = MagicMock(return_value=self.mock_response())
        resp = self.cmd.set_high_purge(False)
        self.assertTrue(resp.message(), "OK")

    def test_set_high_purge_enum(self):
        Response.check_resp = MagicMock(return_value=self.mock_response())
        resp = self.cmd.set_high_purge(HighPurgeState.On)
        self.assertTrue(resp.message(), "OK")

if __name__ == '__main__':
    unittest.main()