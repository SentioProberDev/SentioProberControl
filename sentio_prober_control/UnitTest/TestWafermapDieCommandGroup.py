import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber


class TestWafermapDieCommandGroup(unittest.TestCase):
    def setUp(self):
        """Mock the communicator and initialize the test prober."""
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.test_prober = SentioProber(self.mock_comm)

    def test_add_die(self):
        """Test adding a die"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.die.add(2, 3)
        self.mock_comm.send.assert_called_with("map:die:add 2, 3")

    def test_remove_die(self):
        """Test removing a die"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.die.remove(2, 3)
        self.mock_comm.send.assert_called_with("map:die:remove 2, 3")

    def test_select_die(self):
        """Test selecting a die"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.die.select(2, 3)
        self.mock_comm.send.assert_called_with("map:die:select 2, 3")

    def test_unselect_die(self):
        """Test unselecting a die"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.die.unselect(2, 3)
        self.mock_comm.send.assert_called_with("map:die:unselect 2, 3")

    def test_get_status(self):
        """Test retrieving die status"""
        self.mock_comm.read_line.return_value = "0,0,1"
        result = self.test_prober.map.die.get_status(2, 3)
        self.mock_comm.send.assert_called_with("map:die:get_status 2, 3")
        self.assertEqual(result, 1)  # 1 = Die is selected

    def test_get_current_index(self):
        """Test retrieving current die index"""
        self.mock_comm.read_line.return_value = "0,0,5,6,7"
        result = self.test_prober.map.die.get_current_index()
        self.mock_comm.send.assert_called_with("map:die:get_current_index")
        self.assertEqual(result, (5, 6, 7))

    def test_get_current_subsite(self):
        """Test retrieving current active subsite"""
        self.mock_comm.read_line.return_value = "0,0,2"
        result = self.test_prober.map.die.get_current_subsite()
        self.mock_comm.send.assert_called_with("map:die:get_current_subsite")
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
