import unittest
from unittest.mock import MagicMock, patch
from sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup import LoaderCommandGroup
from sentio_prober_control.Sentio.Enumerations import LoaderStation, OrientationMarker, WaferStatusItem


class TestLoaderCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_parent = MagicMock()
        self.mock_comm = MagicMock()
        self.mock_parent.comm = self.mock_comm
        self.loader = LoaderCommandGroup(self.mock_parent)

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_has_station(self, mock_check):
        mock_check.return_value.message.return_value = "1"
        result = self.loader.has_station(LoaderStation.Cassette1)
        self.assertTrue(result)
        self.mock_comm.send.assert_called_with("loader:has_station cas1")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_load_wafer(self, mock_check):
        mock_check.return_value.message.return_value = "OK"
        msg = self.loader.load_wafer(LoaderStation.Cassette1, 1, 180)
        self.assertEqual(msg, "OK")
        self.mock_comm.send.assert_called_with("loader:load_wafer cas1, 1, 180")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_prealign(self, mock_check):
        mock_check.return_value.message.return_value = "Aligned"
        msg = self.loader.prealign(OrientationMarker.Notch, 90)
        self.assertEqual(msg, "Aligned")
        self.mock_comm.send.assert_called_with("loader:prealign Notch, 90")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_query_wafer_status(self, mock_check):
        mock_check.return_value.message.return_value = "Cassette1,1,200,90,50.0"
        result = self.loader.query_wafer_status(LoaderStation.Cassette1, 1)
        self.assertEqual(result, (LoaderStation.Cassette1, 1, 200, 90, 50.0))

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_scan_station(self, mock_check):
        mock_check.return_value.message.return_value = "11001"
        msg = self.loader.scan_station(LoaderStation.Cassette2)
        self.assertEqual(msg, "11001")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_set_wafer_status(self, mock_check):
        mock_check.return_value.message.return_value = "OK"
        msg = self.loader.set_wafer_status(LoaderStation.Cassette1, 2, WaferStatusItem.Orientation, 180)
        self.assertEqual(msg, "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_start_prepare_station(self, mock_check):
        mock_check.return_value.message.return_value = "OK"
        msg = self.loader.start_prepare_station(LoaderStation.Cassette2, 0)
        self.assertEqual(msg, "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_transfer_wafer(self, mock_check):
        mock_check.return_value.message.return_value = "OK"
        msg = self.loader.transfer_wafer(LoaderStation.Cassette1, 1, LoaderStation.Chuck, 1)
        self.assertEqual(msg, "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_unload_wafer(self, mock_check):
        mock_check.return_value.message.return_value = "OK"
        msg = self.loader.unload_wafer()
        self.assertEqual(msg, "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_has_cassette(self, mock_check):
        mock_check.return_value.message.return_value = "1"
        msg = self.loader.has_cassette(LoaderStation.Cassette2)
        self.assertEqual(msg, "1")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_set_wafer_id(self, mock_check):
        mock_check.return_value.message.return_value = "wafer_123"
        msg = self.loader.set_wafer_id(LoaderStation.Cassette1, 1, "wafer_123")
        self.assertEqual(msg, "wafer_123")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_query_wafer_id(self, mock_check):
        mock_check.return_value.message.return_value = "wafer_123"
        msg = self.loader.query_wafer_id(LoaderStation.Cassette1, 1)
        self.assertEqual(msg, "wafer_123")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_read_wafer_id(self, mock_check):
        mock_check.return_value.message.return_value = "wafer_XYZ"
        msg = self.loader.read_wafer_id("0", "T")
        self.assertEqual(msg, "wafer_XYZ")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_start_prepare_wafer(self, mock_check):
        mock_check.return_value.message.return_value = "OK"
        msg = self.loader.start_prepare_wafer(LoaderStation.Cassette1, 1, 0, 1, LoaderStation.Cassette2, 2)
        self.assertEqual(msg, "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_swap_wafer(self, mock_check):
        mock_check.return_value.message.return_value = "OK"
        msg = self.loader.swap_wafer()
        self.assertEqual(msg, "OK")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_query_station_status(self, mock_check):
        mock_check.return_value.message.return_value = "000111"
        msg = self.loader.query_station_status(LoaderStation.Cassette1)
        self.assertEqual(msg, "000111")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_start_read_wafer_id(self, mock_check):
        mock_check.return_value.message.return_value = "wafer_abc"
        msg = self.loader.start_read_wafer_id("0", "T")
        self.assertEqual(msg, "wafer_abc")

if __name__ == "__main__":
    unittest.main()
