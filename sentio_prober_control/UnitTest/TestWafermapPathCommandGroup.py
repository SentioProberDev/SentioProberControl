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

    def test_add_bins_int(self):
        self.mock_comm.read_line.return_value = "0,0,5"
        result = self.prober.map.path.add_bins(0)
        self.mock_comm.send.assert_called_with("map:path:add_bins 0")
        self.assertEqual(result, 5)

    def test_add_bins_list_int(self):
        self.mock_comm.read_line.return_value = "0,0,3"
        result = self.prober.map.path.add_bins([1, 3, 5])
        self.mock_comm.send.assert_called_with("map:path:add_bins 1,3,5")
        self.assertEqual(result, 3)

    def test_add_bins_range(self):
        self.mock_comm.read_line.return_value = "0,0,4"
        result = self.prober.map.path.add_bins(range(2, 5))
        self.mock_comm.send.assert_called_with("map:path:add_bins 2-4")
        self.assertEqual(result, 4)

    def test_add_bins_list_mixed(self):
        self.mock_comm.read_line.return_value = "0,0,6"
        result = self.prober.map.path.add_bins([range(1, 3), 4, 6])
        self.mock_comm.send.assert_called_with("map:path:add_bins 1-2,4,6")
        self.assertEqual(result, 6)

    def test_remove_bins_int(self):
        self.mock_comm.read_line.return_value = "0,0,6"
        result = self.prober.map.path.remove_bins(2)
        self.mock_comm.send.assert_called_with("map:path:remove_bins 2")
        self.assertEqual(result, 6)

    def test_remove_bins_list(self):
        self.mock_comm.read_line.return_value = "0,0,5"
        result = self.prober.map.path.remove_bins([1, 4, 5])
        self.mock_comm.send.assert_called_with("map:path:remove_bins 1,4,5")
        self.assertEqual(result, 5)

    def test_remove_bins_range(self):
        self.mock_comm.read_line.return_value = "0,0,4"
        result = self.prober.map.path.remove_bins(range(3, 6))  # 3-5
        self.mock_comm.send.assert_called_with("map:path:remove_bins 3-5")
        self.assertEqual(result, 4)

    def test_remove_bins_list_mixed(self):
        self.mock_comm.read_line.return_value = "0,0,7"
        result = self.prober.map.path.remove_bins([range(1, 3), 6, 9])
        self.mock_comm.send.assert_called_with("map:path:remove_bins 1-2,6,9")
        self.assertEqual(result, 7)


if __name__ == "__main__":
    unittest.main()


