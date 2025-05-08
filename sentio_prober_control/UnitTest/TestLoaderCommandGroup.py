import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.Enumerations import LoaderStation, OrientationMarker, WaferStatusItem, RemoteCommandError
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup import LoaderCommandGroup

class TestLoaderCommandGroup(unittest.TestCase):

    def setUp(self):
        self.mock_comm = MagicMock()
        self.mock_parent = MagicMock()
        self.mock_parent.comm = self.mock_comm
        self.loader = LoaderCommandGroup(self.mock_parent)

    def mock_response(self, message="OK"):
        mock_resp = MagicMock()
        mock_resp.message.return_value = message
        return mock_resp

    def test_has_station_true(self):
        self.mock_comm.read_line.return_value = "0,0,1"
        Response.check_resp = MagicMock(return_value=self.mock_response("1"))
        result = self.loader.has_station(LoaderStation.Cassette1)
        self.assertTrue(result)

    def test_scan_station_returns_string(self):
        self.mock_comm.read_line.return_value = "0,0,data"
        Response.check_resp = MagicMock(return_value=self.mock_response("data"))
        result = self.loader.scan_station(LoaderStation.Cassette1)
        self.assertEqual(result, "data")

    def test_load_wafer_with_angle(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        Response.check_resp = MagicMock(return_value=self.mock_response("OK"))
        self.loader.load_wafer(LoaderStation.WaferWallet, 1, 90)
        self.mock_comm.send.assert_called_with("loader:load_wafer ww, 1, 90")

    def test_load_wafer_without_angle(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        Response.check_resp = MagicMock(return_value=self.mock_response("OK"))
        self.loader.load_wafer(LoaderStation.WaferWallet, 1)
        self.mock_comm.send.assert_called_with("loader:load_wafer ww, 1")

    def test_query_wafer_status_returns_tuple(self):
        self.mock_comm.read_line.return_value = "0,0,Cassette1,1,200,180,90"
        Response.check_resp = MagicMock(return_value=self.mock_response("Cassette1,1,200,180,90"))
        result = self.loader.query_wafer_status(LoaderStation.Cassette1, 1)
        self.assertEqual(result[0], LoaderStation.Cassette1)
        self.assertEqual(result[1], 1)
        self.assertEqual(result[2], 200)
        self.assertEqual(result[3], 180)
        self.assertEqual(result[4], 90.0)

    def test_query_wafer_status_returns_none(self):
        class FakeProberException(ProberException):  # ← 繼承 ProberException
            def __init__(self, err):
                self._err = err

            def error(self):
                return self._err

        def raise_empty(*args, **kwargs):
            raise FakeProberException(RemoteCommandError.SlotOrStationEmpty)

        Response.check_resp = MagicMock(side_effect=raise_empty)
        result = self.loader.query_wafer_status(LoaderStation.Cassette1, 1)
        self.assertIsNone(result)

    def test_prealign(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        Response.check_resp = MagicMock(return_value=self.mock_response("OK"))
        self.loader.prealign(OrientationMarker.Notch, 180)
        self.mock_comm.send.assert_called_with("loader:prealign Notch, 180")

    def test_set_wafer_status(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        Response.check_resp = MagicMock(return_value=self.mock_response("OK"))
        self.loader.set_wafer_status(LoaderStation.Cassette1, 5, WaferStatusItem.Progress, 80.0)
        self.mock_comm.send.assert_called_with("loader:set_wafer_status cas1,5,Progress,80.0")

    def test_transfer_wafer(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        Response.check_resp = MagicMock(return_value=self.mock_response("OK"))
        self.loader.transfer_wafer(LoaderStation.Cassette1, 1, LoaderStation.Chuck, 1)
        self.mock_comm.send.assert_called_with("loader:transfer_wafer cas1, 1, chuck, 1")

    def test_unload_wafer(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        Response.check_resp = MagicMock(return_value=self.mock_response("OK"))
        self.loader.unload_wafer()
        self.mock_comm.send.assert_called_with("loader:unload_wafer")

if __name__ == '__main__':
    unittest.main()