import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Enumerations import RoutingPriority, RoutingStartPoint, TestSelection, \
    RoutingPriority, PathSelection


class TestWafermapPathCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.prober = SentioProber(self.mock_comm)

    def test_create_from_bin_with_int(self):
        self.mock_comm.read_line.return_value = "0,0,5"
        result = self.prober.map.path.create_from_bin(5)
        self.mock_comm.send.assert_called_with("map:path:create_from_bins 5")
        self.assertEqual(result, 5)

    def test_create_from_bin_with_str(self):
        self.mock_comm.read_line.return_value = "0,0,20"
        result = self.prober.map.path.create_from_bin("0-1")
        self.mock_comm.send.assert_called_with("map:path:create_from_bins 0-1")
        self.assertEqual(result, 20)

    def test_create_from_bin_with_enum(self):
        self.mock_comm.read_line.return_value = "0,0,1"
        result = self.prober.map.path.create_from_bin(PathSelection.Fail)
        self.mock_comm.send.assert_called_with("map:path:create_from_bins fail")
        self.assertEqual(result, 1)

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

    def test_add_bins_str(self):
        self.mock_comm.read_line.return_value = "0,0,12"
        result = self.prober.map.path.add_bins("1-5")
        self.mock_comm.send.assert_called_with("map:path:add_bins 1-5")
        self.assertEqual(result, 12)

    def test_add_bins_int(self):
        self.mock_comm.read_line.return_value = "0,0,5"
        result = self.prober.map.path.add_bins(0)
        self.mock_comm.send.assert_called_with("map:path:add_bins 0")
        self.assertEqual(result, 5)

    def test_add_bins_enum(self):
        self.mock_comm.read_line.return_value = "0,0,20"
        result = self.prober.map.path.add_bins(PathSelection.Pass)
        self.mock_comm.send.assert_called_with("map:path:add_bins pass")
        self.assertEqual(result, 20)

    def test_remove_enum(self):
        self.mock_comm.read_line.return_value = "0,0,6"
        result = self.prober.map.path.remove_bins("Fail")
        self.mock_comm.send.assert_called_with("map:path:remove_bins Fail")
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()


