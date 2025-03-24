import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Enumerations import RoutingPriority, RoutingStartPoint, TestSelection, RoutingPriority


class TestWafermapPathCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.prober = SentioProber(self.mock_comm)

    def test_create_from_bin(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.path.create_from_bin(3)
        self.mock_comm.send.assert_called_with("map:path:create_from_bins 3")

    def test_get_die(self):
        self.mock_comm.read_line.return_value = "0,0,10,20"
        result = self.prober.map.path.get_die(5)
        self.mock_comm.send.assert_called_with("map:path:get_die 5")
        self.assertEqual(result, (10, 20))

    def test_select_dies(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.path.select_dies(TestSelection.All)
        self.mock_comm.send.assert_called_with("map:path:select_dies a")

    def test_set_routing(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.path.set_routing(RoutingStartPoint.UpperLeft, RoutingPriority.RowUniDir)
        self.mock_comm.send.assert_called_with("map:set_routing ul, r")

    def test_add_bins(self):
        self.mock_comm.read_line.return_value = "0,0,12"
        result = self.prober.map.path.add_bins("1-5")
        self.mock_comm.send.assert_called_with("map:path:add_bins 1-5")
        self.assertEqual(result, 12)

    def test_remove_bins(self):
        self.mock_comm.read_line.return_value = "0,0,6"
        result = self.prober.map.path.remove_bins("Fail")
        self.mock_comm.send.assert_called_with("map:path:remove_bins Fail")
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()


