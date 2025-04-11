import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Sentio.Response import Response

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

    def test_get_indexer_pos(self):
        self.mock_comm.read_line.return_value = "0,0,3,down"
        location, position = self.test_prober.get_indexer_pos()
        self.mock_comm.send.assert_called_with("get_indexer_pos")
        self.assertEqual(location, 3)
        self.assertEqual(position, "down")

    def test_indexer_cda_on(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.indexer_cda(True)
        self.mock_comm.send.assert_called_with("indexer_cda on")
        self.assertIsInstance(resp, Response)

    def test_move_bottom_platen_contact(self):
        self.mock_comm.read_line.return_value = "0,0,1500"
        z = self.test_prober.move_bottom_platen_contact()
        self.mock_comm.send.assert_called_with("move_bottom_platen_contact")
        self.assertEqual(z, 1500.0)

    def test_move_bottom_platen_separation(self):
        self.mock_comm.read_line.return_value = "0,0,500"
        z = self.test_prober.move_bottom_platen_separation()
        self.mock_comm.send.assert_called_with("move_bottom_platen_separation")
        self.assertEqual(z, 500.0)

    def test_move_indexer_lift(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.move_indexer_lift()
        self.mock_comm.send.assert_called_with("move_indexer_lift")
        self.assertIsInstance(resp, Response)

    def test_move_indexer_down(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.move_indexer_down()
        self.mock_comm.send.assert_called_with("move_indexer_down")
        self.assertIsInstance(resp, Response)

    def test_probe_air_lift(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.probe_air_lift("v1", "lift")
        self.mock_comm.send.assert_called_with("probe_air_lift v1,lift")
        self.assertIsInstance(resp, Response)

    def test_set_signal_tower(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.set_signal_tower(1, 0, 2, -1)
        self.mock_comm.send.assert_called_with("set_signal_tower 1,0,2,-1")
        self.assertIsInstance(resp, Response)

    def test_set_signal_tower_buzzer(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.set_signal_tower_buzzer(2)
        self.mock_comm.send.assert_called_with("set_signal_tower_buzzer 2")
        self.assertIsInstance(resp, Response)

    def test_start_move_indexer_pos(self):
        self.mock_comm.read_line.return_value = "0,123,OK"
        resp = self.test_prober.start_move_indexer_pos(4)
        self.mock_comm.send.assert_called_with("start_move_indexer_pos 4")
        self.assertIsInstance(resp, Response)

    def test_swap_bridge(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.swap_bridge("right", "up")
        self.mock_comm.send.assert_called_with("swap_bridge right,up")
        self.assertIsInstance(resp, Response)

    def test_get_door_status_closed_locked(self):
        self.mock_comm.read_line.return_value = "0,0,1,1"
        closed, locked = self.test_prober.get_door_status("prober")
        self.mock_comm.send.assert_called_with("get_door_status prober")
        self.assertTrue(closed)
        self.assertTrue(locked)

    def test_get_door_status_open_unlocked(self):
        self.mock_comm.read_line.return_value = "0,0,0,0"
        closed, locked = self.test_prober.get_door_status("loader")
        self.mock_comm.send.assert_called_with("get_door_status loader")
        self.assertFalse(closed)
        self.assertFalse(locked)

    def test_set_door_lock_lock(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.set_door_lock("prober", True)
        self.mock_comm.send.assert_called_with("set_door_lock prober,1")
        self.assertIsInstance(resp, Response)

    def test_set_door_lock_unlock(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.test_prober.set_door_lock("loader", False)
        self.mock_comm.send.assert_called_with("set_door_lock loader,0")
        self.assertIsInstance(resp, Response)


if __name__ == "__main__":
    unittest.main()
