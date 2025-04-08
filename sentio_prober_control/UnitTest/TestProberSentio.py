import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Sentio.Response import Response

from sentio_prober_control.Sentio.Enumerations import (
    ChuckPositionHint,
    ChuckSite,
    ChuckSpeed,
    VacuumState,
    HighPowerAirState,
    SoftContactState,
    UserCoordState
)

class TestScopeCommandGroup(unittest.TestCase):
    def setUp(self):
        """Initialize the mock communicator and ScopeCommandGroup instance."""
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)

        # Ensure the mock provides `send` and `read_line` methods
        self.test_prober = SentioProber(self.mock_comm)

    def test_get_scope_home(self):
        """Test get_scope_home method."""
        self.mock_comm.read_line.return_value = "0,0,250,250"
        home_x, home_y = self.test_prober.get_scope_home()
        self.mock_comm.send.assert_called_with("get_scope_home")
        self.assertEqual(home_x, 250.0)
        self.assertEqual(home_y, 250.0)

    def test_set_scope_home_with_values(self):
        """Test set_scope_home method with specified X and Y values."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        response = self.test_prober.set_scope_home(300, 400)
        self.mock_comm.send.assert_called_with("set_scope_home 300,400")
        self.assertIsNone(response)  # The method does not return a value

    def test_set_scope_home_without_values(self):
        """Test set_scope_home method with no arguments (default to current position)."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        response = self.test_prober.set_scope_home()
        self.mock_comm.send.assert_called_with("set_scope_home")
        self.assertIsNone(response)

    def test_step_scope_site(self):
        """Test step_scope_site method."""
        self.mock_comm.read_line.return_value = "0,0,Pos1,1000,2000"
        site_id, offset_x, offset_y = self.test_prober.step_scope_site(2)
        self.mock_comm.send.assert_called_with("step_scope_site 2")
        self.assertEqual(site_id, "Pos1")
        self.assertEqual(offset_x, 1000.0)
        self.assertEqual(offset_y, 2000.0)

    def test_step_scope_site_first(self):
        """Test step_scope_site_first method."""
        self.mock_comm.read_line.return_value = "0,0,Pos1,0,0"
        site_id, offset_x, offset_y = self.test_prober.step_scope_site_first()
        self.mock_comm.send.assert_called_with("step_scope_site_first")
        self.assertEqual(site_id, "Pos1")
        self.assertEqual(offset_x, 0.0)
        self.assertEqual(offset_y, 0.0)

    def test_step_scope_site_next(self):
        """Test step_scope_site_next method."""
        self.mock_comm.read_line.return_value = "0,0,Pos2,1000,1000"
        site_id, offset_x, offset_y = self.test_prober.step_scope_site_next()
        self.mock_comm.send.assert_called_with("step_scope_site_next")
        self.assertEqual(site_id, "Pos2")
        self.assertEqual(offset_x, 1000.0)
        self.assertEqual(offset_y, 1000.0)

    def test_get_chuck_position_hint(self):
        """Test get_chuck_position_hint returns correct enums."""
        self.mock_comm.read_line.return_value = "0,0,Probing,Wafer"
        position, site = self.test_prober.get_chuck_position_hint()
        self.mock_comm.send.assert_called_with("get_chuck_position_hint")
        self.assertEqual(position, ChuckPositionHint.Center)
        self.assertEqual(site, ChuckSite.Wafer)

    def test_get_chuck_site_count(self):
        """Test get_chuck_site_count returns correct integer."""
        self.mock_comm.read_line.return_value = "0,0,5"
        count = self.test_prober.get_chuck_site_count()
        self.mock_comm.send.assert_called_with("get_chuck_site_count")
        self.assertEqual(count, 5)

    def test_get_chuck_site_index_without_name(self):
        """Test get_chuck_site_index without argument returns correct index."""
        self.mock_comm.read_line.return_value = "0,0,2"
        index = self.test_prober.get_chuck_site_index()
        self.mock_comm.send.assert_called_with("get_chuck_site_index")
        self.assertEqual(index, 2)

    def test_get_chuck_site_index_with_name(self):
        """Test get_chuck_site_index with a site name returns correct index."""
        self.mock_comm.read_line.return_value = "0,0,3"
        index = self.test_prober.get_chuck_site_index("Wafer")
        self.mock_comm.send.assert_called_with("get_chuck_site_index Wafer")
        self.assertEqual(index, 3)

    def test_get_chuck_site_name_without_index(self):
        """Test get_chuck_site_name with no index."""
        self.mock_comm.read_line.return_value = "0,0,Wafer"
        result = self.test_prober.get_chuck_site_name()
        self.mock_comm.send.assert_called_with("get_chuck_site_name")
        self.assertEqual(result, ChuckSite.Wafer)

    def test_get_chuck_site_name_with_index(self):
        """Test get_chuck_site_name with specific index."""
        self.mock_comm.read_line.return_value = "0,0,AuxLeft"
        result = self.test_prober.get_chuck_site_name(2)
        self.mock_comm.send.assert_called_with("get_chuck_site_name 2")
        self.assertEqual(result, ChuckSite.AuxLeft)

    def test_get_chuck_site_pos_with_site(self):
        """Test get_chuck_site_pos with ChuckSite enum."""
        self.mock_comm.read_line.return_value = "0,0,25000,40000,-45"
        x, y, theta = self.test_prober.get_chuck_site_pos(ChuckSite.Wafer)
        self.mock_comm.send.assert_called_with("get_chuck_site_pos Wafer")
        self.assertEqual(x, 25000.0)
        self.assertEqual(y, 40000.0)
        self.assertEqual(theta, -45.0)

    def test_get_chuck_site_pos_without_site(self):
        """Test get_chuck_site_pos without site (use current active site)."""
        self.mock_comm.read_line.return_value = "0,0,1000,2000,15"
        x, y, theta = self.test_prober.get_chuck_site_pos()
        self.mock_comm.send.assert_called_with("get_chuck_site_pos")
        self.assertEqual(x, 1000.0)
        self.assertEqual(y, 2000.0)
        self.assertEqual(theta, 15.0)

    def test_get_chuck_speed(self):
        """Test get_chuck_speed returns correct ChuckSpeed enum."""
        self.mock_comm.read_line.return_value = "0,0,Fast"
        result = self.test_prober.get_chuck_speed()
        self.mock_comm.send.assert_called_with("get_chuck_speed")
        self.assertEqual(result, ChuckSpeed.Fast)

    def test_get_vacuum_status_on_with_site(self):
        """Test get_vacuum_status returns ON with ChuckSite specified."""
        self.mock_comm.read_line.return_value = "0,0,1"
        result = self.test_prober.get_vacuum_status(ChuckSite.AuxLeft)
        self.mock_comm.send.assert_called_with("get_vacuum_status AuxLeft")
        self.assertEqual(result, VacuumState.On)

    def test_get_vacuum_status_off_with_site(self):
        """Test get_vacuum_status returns OFF with ChuckSite specified."""
        self.mock_comm.read_line.return_value = "0,0,0"
        result = self.test_prober.get_vacuum_status(ChuckSite.Wafer)
        self.mock_comm.send.assert_called_with("get_vacuum_status Wafer")
        self.assertEqual(result, VacuumState.Off)

    def test_get_vacuum_status_without_site(self):
        """Test get_vacuum_status returns ON using current active site."""
        self.mock_comm.read_line.return_value = "0,0,1"
        result = self.test_prober.get_vacuum_status()
        self.mock_comm.send.assert_called_with("get_vacuum_status")
        self.assertEqual(result, VacuumState.On)

    def test_move_chuck_hover(self):
        """Test move_chuck_hover returns correct Z position."""
        self.mock_comm.read_line.return_value = "0,0,16000.0"
        z = self.test_prober.move_chuck_hover()
        self.mock_comm.send.assert_called_with("move_chuck_hover")
        self.assertEqual(z, 16000.0)

    def test_move_chuck_index(self):
        """Test move_chuck_index returns correct new XY position."""
        self.mock_comm.read_line.return_value = "0,0,1000.0,3000.0"
        x, y = self.test_prober.move_chuck_index("Home", 5, -3)
        self.mock_comm.send.assert_called_with("move_chuck_index Home, 5, -3")
        self.assertEqual(x, 1000.0)
        self.assertEqual(y, 3000.0)

    def test_move_chuck_xyt(self):
        """Test move_chuck_xyt sends correct command and completes without error."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.move_chuck_xyt(5.0, -10.0, 0.5)
        self.mock_comm.send.assert_called_with("move_chuck_xyt 5.0, -10.0, 0.5")
        self.assertIsNone(result)

    def test_set_chuck_overtravel_gap(self):
        """Test set_chuck_overtravel_gap sends correct command and succeeds."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_chuck_overtravel_gap(50.0)
        self.mock_comm.send.assert_called_with("set_chuck_overtravel_gap 50.0")
        self.assertIsNone(result)

    def test_set_chuck_separation_gap(self):
        """Test set_chuck_separation_gap sends correct command and succeeds."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_chuck_separation_gap(250.0)
        self.mock_comm.send.assert_called_with("set_chuck_separation_gap 250.0")
        self.assertIsNone(result)

    def test_set_chuck_site_overtravel_gap_valid_site(self):
        """Test setting overtravel gap with valid ChuckSite."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_chuck_site_overtravel_gap(ChuckSite.AuxRight, 12.5)
        self.mock_comm.send.assert_called_with("set_chuck_site_overtravel_gap AuxRight, 12.5")
        self.assertIsNone(result)

    def test_set_chuck_site_pos_with_enum(self):
        """Test set_chuck_site_pos with all values and ChuckSite enum."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_chuck_site_pos(1000.0, 2000.0, 10.0, ChuckSite.Wafer)
        self.mock_comm.send.assert_called_with("set_chuck_site_pos Wafer,1000.0,2000.0,10.0")
        self.assertIsNone(result)

    def test_set_chuck_site_pos_without_site(self):
        """Test set_chuck_site_pos with x, y, theta only (uses current site)."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_chuck_site_pos(500.0, 500.0, 0.0)
        self.mock_comm.send.assert_called_with("set_chuck_site_pos 500.0,500.0,0.0")
        self.assertIsNone(result)

    def test_set_chuck_site_pos_with_no_arguments(self):
        """Test set_chuck_site_pos with no arguments (uses current site and position)."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_chuck_site_pos()
        self.mock_comm.send.assert_called_with("set_chuck_site_pos")
        self.assertIsNone(result)

    def test_set_chuck_site_separation_gap_with_site(self):
        """Test setting separation gap with ChuckSite enum."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_chuck_site_separation_gap(ChuckSite.AuxRight, 250.0)
        self.mock_comm.send.assert_called_with("set_chuck_site_separation_gap AuxRight, 250.0")
        self.assertIsNone(result)

    def test_set_high_power_air_on(self):
        """Test setting high power air to ON."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_high_power_air(HighPowerAirState.On)
        self.mock_comm.send.assert_called_with("set_high_power_air 1")
        self.assertIsNone(result)

    def test_set_high_power_air_off(self):
        """Test setting high power air to OFF."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_high_power_air(HighPowerAirState.Off)
        self.mock_comm.send.assert_called_with("set_high_power_air 0")
        self.assertIsNone(result)

    def test_set_high_power_air_none_raises(self):
        """Test that passing None raises ValueError."""
        with self.assertRaises(ValueError):
            self.test_prober.set_high_power_air(None)

    def test_set_soft_contact_enable(self):
        """Test enabling soft contact."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_soft_contact(SoftContactState.Enable)
        self.mock_comm.send.assert_called_with("set_soft_contact 1")
        self.assertIsNone(result)

    def test_set_soft_contact_disable(self):
        """Test disabling soft contact."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_soft_contact(SoftContactState.Disable)
        self.mock_comm.send.assert_called_with("set_soft_contact 0")
        self.assertIsNone(result)

    def test_set_soft_contact_none_raises(self):
        """Test passing None raises ValueError."""
        with self.assertRaises(ValueError):
            self.test_prober.set_soft_contact(None)

    def test_set_user_coordinate_origin_chuck(self):
        """Test setting user coordinate origin for chuck."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_user_coordinate_origin(UserCoordState.Chuck, 0.0, 0.0)
        self.mock_comm.send.assert_called_with("set_user_coordinate_origin chuck,0.0,0.0")
        self.assertIsNone(result)

    def test_set_user_coordinate_origin_scope(self):
        """Test setting user coordinate origin for scope."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.test_prober.set_user_coordinate_origin(UserCoordState.Scope, 150.0, 300.0)
        self.mock_comm.send.assert_called_with("set_user_coordinate_origin scope,150.0,300.0")
        self.assertIsNone(result)

    def test_set_user_coordinate_origin_none_raises(self):
        """Test that passing None as state raises ValueError."""
        with self.assertRaises(ValueError):
            self.test_prober.set_user_coordinate_origin(None, 0.0, 0.0)

    def test_create_project_with_full_path(self):
        """Test create_project using full directory path."""
        self.mock_comm.read_line.return_value = "0,0,C:\\Users\\Project1\\Project1.trex"
        result = self.test_prober.create_project("C:\\Users\\Project1")
        self.mock_comm.send.assert_called_with("create_project C:\\Users\\Project1")
        self.assertEqual(result, "C:\\Users\\Project1\\Project1.trex")

    def test_create_project_with_name_only(self):
        """Test create_project using just project name (default directory)."""
        self.mock_comm.read_line.return_value = "0,0,Default project directory\\ProjectX\\ProjectX.trex"
        result = self.test_prober.create_project("ProjectX")
        self.mock_comm.send.assert_called_with("create_project ProjectX")
        self.assertEqual(result, "Default project directory\\ProjectX\\ProjectX.trex")


if __name__ == "__main__":
    unittest.main()
