import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.Enumerations import LoaderStation, OrientationMarker, WaferStatusItem
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup import LoaderCommandGroup

class TestLoaderCommandGroup(unittest.TestCase):
    def setUp(self):
        """初始化 LoaderCommandGroup 測試環境"""
        self.mock_comm = MagicMock()  # 建立 Mock 通訊物件
        self.loader = LoaderCommandGroup(self.mock_comm)  # 傳入 Mock 通訊物件
        self.mock_comm.send = MagicMock()
        self.mock_comm.read_line = MagicMock()

    def test_has_station(self):
        """測試 has_station() 是否正確回應"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,1"  # 模擬 Prober Response
        self.assertTrue(self.loader.has_station(station))
        self.mock_comm.send.assert_called_with(f"loader:has_station {station.toSentioAbbr()}")

    def test_load_wafer(self):
        """測試 load_wafer() 指令"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.loader.load_wafer(station, 1)
        self.mock_comm.send.assert_called_with(f"loader:load_wafer {station.toSentioAbbr()}, 1")

    def test_prealign(self):
        """測試 prealign() 指令"""
        marker = OrientationMarker.Notch
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.loader.prealign(marker, 90)
        self.mock_comm.send.assert_called_with(f"loader:prealign {marker.toSentioAbbr()}, 90")

    def test_query_wafer_status(self):
        """測試 query_wafer_status() 指令"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,Cassette1,1,200,0,50"
        result = self.loader.query_wafer_status(station, 1)
        self.assertEqual(result, (LoaderStation.Cassette1, 1, 200, 0, 50.0))
        self.mock_comm.send.assert_called_with(f"loader:query_wafer_status {station.toSentioAbbr()}, 1")

    def test_scan_station(self):
        """測試 scan_station() 指令"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.loader.scan_station(station)
        self.mock_comm.send.assert_called_with(f"loader:scan_station {station.toSentioAbbr()}")

    def test_set_wafer_status(self):
        """測試 set_wafer_status() 指令"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.loader.set_wafer_status(station, 1, WaferStatusItem.Progress, 100.0)
        self.mock_comm.send.assert_called_with(f"loader:set_wafer_status {station.toSentioAbbr()},1,Progress,100.0")

    def test_transfer_wafer(self):
        """測試 transfer_wafer() 指令"""
        src_station = LoaderStation.Cassette1
        dst_station = LoaderStation.Cassette2
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.loader.transfer_wafer(src_station, 1, dst_station, 2)
        self.mock_comm.send.assert_called_with(
            f"loader:transfer_wafer {src_station.toSentioAbbr()}, 1, {dst_station.toSentioAbbr()}, 2"
        )

    def test_unload_wafer(self):
        """測試 unload_wafer() 指令"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.loader.unload_wafer()
        self.mock_comm.send.assert_called_with("loader:unload_wafer")

    def test_has_cassette(self):
        """測試 has_cassette() 指令"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,1"
        self.assertEqual(self.loader.has_cassette(station), "1")
        self.mock_comm.send.assert_called_with(f"loader:has_cassette {station.toSentioAbbr()}")

    def test_set_wafer_id(self):
        """測試 set_wafer_id() 指令"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.loader.set_wafer_id(station, 1, "TestWafer123")
        self.mock_comm.send.assert_called_with(f"loader:set_wafer_id {station.toSentioAbbr()}, 1, TestWafer123")

    def test_query_wafer_id(self):
        """測試 query_wafer_id() 指令"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,TestWafer123"
        result = self.loader.query_wafer_id(station, 1)
        self.assertEqual(result, "TestWafer123")
        self.mock_comm.send.assert_called_with(f"loader:query_wafer_id {station.toSentioAbbr()}, 1")

    def test_read_wafer_id(self):
        """測試 read_wafer_id() 指令"""
        self.mock_comm.read_line.return_value = "0,0,TestWafer123"
        result = self.loader.read_wafer_id("180", "T")
        self.assertEqual(result, "TestWafer123")
        self.mock_comm.send.assert_called_with("loader:read_wafer_id 180, T")

    def test_query_station_status(self):
        """測試 query_station_status() 指令"""
        station = LoaderStation.Cassette1
        self.mock_comm.read_line.return_value = "0,0,OK"
        result = self.loader.query_station_status(station)
        self.assertEqual(result, "OK")
        self.mock_comm.send.assert_called_with(f"loader:query_station_status {station.toSentioAbbr()}")

    def test_start_read_wafer_id(self):
        """測試 start_read_wafer_id() 指令"""
        self.mock_comm.read_line.return_value = "0,0,TestWafer123"
        result = self.loader.start_read_wafer_id("180", "T")
        self.assertEqual(result, "TestWafer123")
        self.mock_comm.send.assert_called_with("loader:start_read_wafer_id 180, T")

if __name__ == "__main__":
    unittest.main()
