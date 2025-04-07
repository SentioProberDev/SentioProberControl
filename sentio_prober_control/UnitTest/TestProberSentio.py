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


if __name__ == "__main__":
    unittest.main()
