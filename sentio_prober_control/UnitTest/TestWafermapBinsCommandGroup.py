import unittest
from unittest.mock import MagicMock

from sentio_prober_control.Sentio.Enumerations import BinQuality, BinSelection

from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber


class TestWafermapBinsCommandGroup(unittest.TestCase):
    def setUp(self):
        """Mock the communicator and initialize the test prober."""
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.test_prober = SentioProber(self.mock_comm)

    def test_clear_all(self):
        """Test clearing all bins"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.bins.clear_all()
        self.mock_comm.send.assert_called_with("map:bins:clear_all")

    def test_clear_all_values(self):
        """Test clearing all bin values"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.bins.clear_all_values()
        self.mock_comm.send.assert_called_with("map:bins:clear_all_values")

    def test_get_bin(self):
        """Test getting bin information of a die"""
        self.mock_comm.read_line.return_value = "0,0,5"
        result = self.test_prober.map.bins.get_bin(2, 3)
        self.mock_comm.send.assert_called_with("map:bins:get_bin 2, 3")
        self.assertEqual(result, 5)

    def test_get_bin_info(self):
        """Test getting bin information"""
        self.mock_comm.read_line.return_value = "0,0,3,TestBin,Pass,#FF00FFFF"
        result = self.test_prober.map.bins.get_bin_info(3)
        self.mock_comm.send.assert_called_with("map:bins:get_bin_info 3")
        self.assertEqual(result, (3, "TestBin", BinQuality.Pass, "#FF00FFFF"))

    def test_get_num_bins(self):
        """Test getting the number of bins"""
        self.mock_comm.read_line.return_value = "0,0,10"
        result = self.test_prober.map.bins.get_num_bins()
        self.mock_comm.send.assert_called_with("map:bins:get_num_bins")
        self.assertEqual(result, 10)

    def test_load(self):
        """Test loading binning table from file"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.bins.load("bin_table.xbt")
        self.mock_comm.send.assert_called_with("map:bins:load bin_table.xbt")

    def test_set_all(self):
        """Test setting all bins to a specific value"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.bins.set_all(3, BinSelection.DiesOnly)
        self.mock_comm.send.assert_called_with("map:bins:set_all 3, d")

    def test_set_bin(self):
        """Test setting a specific bin"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.bins.set_bin(2, 4, 5)
        self.mock_comm.send.assert_called_with("map:bins:set_bin 2, 4, 5")

    def test_set_value(self):
        """Test setting a floating-point value on a die"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.bins.set_value(1.5, 2, 3)
        self.mock_comm.send.assert_called_with("map:bins:set_value 1.5, 2, 3")

    def test_resize(self):
        """Test resizing the binning table"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.bins.resize(3)
        self.mock_comm.send.assert_called_with("map:bins:resize 3")

    def test_set_bin_info(self):
        """Test setting bin information"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.bins.set_bin_info(5, "GoodBin", BinQuality.Pass, "#FF00FFFF")
        self.mock_comm.send.assert_called_with("map:bins:set_bin_info 5, GoodBin, pass, #FF00FFFF")


if __name__ == "__main__":
    unittest.main()
