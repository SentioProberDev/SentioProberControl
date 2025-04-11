import unittest
from unittest.mock import MagicMock, patch
from sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup import StatusCommandGroup
from sentio_prober_control.Sentio.Enumerations import ThermoChuckState, ChuckThermoEnergyMode
from sentio_prober_control.Sentio.Enumerations import ChuckThermoHoldMode, HighPurgeState


class TestStatusCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_parent = MagicMock()
        self.mock_comm = MagicMock()
        self.mock_parent.comm = self.mock_comm
        self.status = StatusCommandGroup(self.mock_parent)

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_get_chuck_temp(self, mock_resp):
        mock_resp.return_value.message.return_value = "30.5,OK"
        self.assertEqual(self.status.get_chuck_temp(), 30.5)

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_get_chuck_temp_setpoint(self, mock_resp):
        mock_resp.return_value.message.return_value = "25.0,OK"
        self.assertEqual(self.status.get_chuck_temp_setpoint(), 25.0)

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_get_chuck_thermo_state(self, mock_resp):
        cases = {
            "soaking": ThermoChuckState.Soaking,
            "cooling": ThermoChuckState.Cooling,
            "heating": ThermoChuckState.Heating,
            "controlling": ThermoChuckState.Controlling,
            "standby": ThermoChuckState.Standby,
            "error": ThermoChuckState.Error,
            "uncontrolled": ThermoChuckState.Uncontrolled,
            "unknown stuff": ThermoChuckState.Unknown,
        }
        for msg, expected in cases.items():
            mock_resp.return_value.message.return_value = msg
            self.assertEqual(self.status.get_chuck_thermo_state(), expected)

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_get_machine_status(self, mock_resp):
        mock_resp.return_value.message.return_value = "0,0,Ready,IsMeasuring,LoaderBusy"
        self.assertEqual(self.status.get_machine_status(), (True, True, True))

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_get_soaking_time(self, mock_resp):
        mock_resp.return_value.message.return_value = "120.0"
        self.assertEqual(self.status.get_soaking_time(80.0), 120.0)

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_set_chuck_temp(self, mock_resp):
        mock_resp.return_value = MagicMock()
        self.status.comm.send = MagicMock()
        self.status.set_chuck_temp(75.0)
        self.status.comm.send.assert_called_with("status:set_chuck_temp 75.00, False")
        mock_resp.assert_called()

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_get_chuck_thermo_energy_mode(self, mock_resp):
        mock_resp.return_value.message.return_value = "Fast"
        self.assertEqual(self.status.get_chuck_thermo_energy_mode(), ChuckThermoEnergyMode.Fast)

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_get_chuck_thermo_hold_mode(self, mock_resp):
        mock_resp.return_value.message.return_value = "Active"
        self.assertEqual(self.status.get_chuck_thermo_hold_mode(), ChuckThermoHoldMode.Active)

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_get_high_purge_state(self, mock_resp):
        mock_resp.return_value.message.return_value = "On"
        self.assertEqual(self.status.get_high_purge_state(), HighPurgeState.On)

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_set_chuck_thermo_energy_mode(self, mock_resp):
        mock_resp.return_value.message.return_value = "OK"
        resp = self.status.set_chuck_thermo_energy_mode("Optimal")
        self.assertEqual(resp.message(), "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_set_chuck_thermo_hold_mode(self, mock_resp):
        mock_resp.return_value.message.return_value = "OK"
        self.status.comm.send = MagicMock()
        resp = self.status.set_chuck_thermo_hold_mode(True)
        self.status.comm.send.assert_called_with("status:set_chuck_thermo_hold_mode Active")
        self.assertEqual(resp.message(), "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_set_chuck_thermo_mode(self, mock_resp):
        mock_resp.return_value.message.return_value = "OK"
        resp = self.status.set_chuck_thermo_mode("Turbo")
        self.assertEqual(resp.message(), "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup.Response.check_resp")
    def test_set_high_purge(self, mock_resp):
        mock_resp.return_value.message.return_value = "OK"
        self.status.comm.send = MagicMock()
        resp = self.status.set_high_purge(True)
        self.status.comm.send.assert_called_with("status:set_high_purge ON")
        self.assertEqual(resp.message(), "OK")

    def test_get_access_level(self):
        self.mock_comm.read_line.return_value = "0,0,Admin"
        self.assertEqual(self.status.get_access_level(), "Admin")

    def test_get_prop(self):
        self.mock_comm.read_line.return_value = "0,0,Wafer"
        self.assertEqual(self.status.get_prop("Active_Stage", "Chuck"), "Wafer")

    def test_get_machine_id(self):
        self.mock_comm.read_line.return_value = "0,0,MPI12345"
        self.assertEqual(self.status.get_machine_id(), "MPI12345")

    def test_get_version(self):
        self.mock_comm.read_line.return_value = "0,0,v1.2.3"
        self.assertEqual(self.status.get_version(), "v1.2.3")

    def test_set_prop(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.status.set_prop("Active_Stage", "Chuck", "Wafer")
        self.assertEqual(resp.message(), "OK")

    def test_show_message(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.assertEqual(self.status.show_message("Confirm?", "YesNo", "ConfirmBox", "Hint"), "OK")

    def test_start_show_message(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.assertEqual(self.status.start_show_message("Start?", "OK", "StartWin", "Warning"), "OK")

if __name__ == "__main__":
    unittest.main()
