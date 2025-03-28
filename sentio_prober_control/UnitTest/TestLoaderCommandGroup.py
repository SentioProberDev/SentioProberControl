import unittest
from unittest.mock import MagicMock, patch

from sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup import LoaderCommandGroup

# 🧰 小工具：建立有 toSentioAbbr() 的 mock enum
def fake_enum(value: str):
    mock_enum = MagicMock()
    mock_enum.toSentioAbbr.return_value = value
    return mock_enum


def mock_response(mock_check, message):
    mock_resp = MagicMock()
    mock_resp.message.return_value = message
    mock_check.return_value = mock_resp


class TestLoaderCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_parent = MagicMock()
        self.mock_comm = MagicMock()
        self.mock_parent.comm = self.mock_comm
        self.loader = LoaderCommandGroup(self.mock_parent)

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_has_station(self, mock_check):
        mock_response(mock_check, "1")
        station = fake_enum("cas1")
        result = self.loader.has_station(station)
        self.assertTrue(result)
        self.mock_comm.send.assert_called_with("loader:has_station cas1")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_load_wafer(self, mock_check):
        mock_response(mock_check, "OK")
        station = fake_enum("cas1")
        self.loader.load_wafer(station, 1, 180)
        self.mock_comm.send.assert_called_with("loader:load_wafer cas1, 1, 180")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_prealign(self, mock_check):
        mock_response(mock_check, "OK")
        marker = fake_enum("Notch")
        self.loader.prealign(marker, 90)
        self.mock_comm.send.assert_called_with("loader:prealign Notch, 90")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_query_wafer_status(self, mock_check):
        mock_response(mock_check, "Cassette1,1,200,90,50.0")
        station = fake_enum("Cassette1")
        result = self.loader.query_wafer_status(station, 1)
        self.assertEqual(result, ("Cassette1", 1, 200, 90, 50.0))

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_set_wafer_status(self, mock_check):
        mock_response(mock_check, "OK")
        station = fake_enum("cas1")
        status_item = fake_enum("Orientation")
        self.loader.set_wafer_status(station, 2, status_item, 180)
        self.mock_comm.send.assert_called_with("loader:set_wafer_status cas1,2,Orientation,180")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_set_wafer_id(self, mock_check):
        mock_response(mock_check, "OK")
        station = fake_enum("cas1")
        self.loader.set_wafer_id(station, 1, "wafer_123")
        self.mock_comm.send.assert_called_with("loader:set_wafer_id cas1, 1, wafer_123")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_query_wafer_id(self, mock_check):
        mock_response(mock_check, "wafer_123")
        station = fake_enum("cas1")
        self.loader.query_wafer_id(station, 1)
        self.mock_comm.send.assert_called_with("loader:query_wafer_id cas1, 1")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_start_prepare_wafer(self, mock_check):
        mock_response(mock_check, "OK")
        s1 = fake_enum("cas1")
        s2 = fake_enum("cas2")
        self.loader.start_prepare_wafer(s1, 1, 0, 1, s2, 2)
        self.mock_comm.send.assert_called_with("loader:start_prepare_wafer cas1, 1, 0, 1, cas2, 2")

    @patch("sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.Response.check_resp")
    def test_query_station_status(self, mock_check):
        mock_response(mock_check, "000111")
        station = fake_enum("cas1")
        self.loader.query_station_status(station)
        self.mock_comm.send.assert_called_with("loader:query_station_status cas1")


if __name__ == "__main__":
    unittest.main()
