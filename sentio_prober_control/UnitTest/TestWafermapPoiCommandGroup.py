import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Enumerations import PoiReferenceXy, Stage


class TestWafermapPoiCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.prober = SentioProber(self.mock_comm)

    def test_add(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.poi.add(100.0, 200.0, "MyPOI")
        self.mock_comm.send.assert_called_with("map:poi:add 100.0, 200.0, MyPOI")

    def test_poi_get(self):
        self.mock_comm.read_line.return_value = "0,0,123.45,678.90,MyPOI"
        result = self.prober.map.poi.get(2)
        self.mock_comm.send.assert_called_with("map:poi:get 2")
        self.assertEqual(result, (123.45, 678.90, "MyPOI"))

    def test_get_num(self):
        self.mock_comm.read_line.return_value = "0,0,5"
        result = self.prober.map.poi.get_num()
        self.mock_comm.send.assert_called_with("map:poi:get_num")
        self.assertEqual(result, 5)

    def test_reset(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.poi.reset(Stage.Chuck, PoiReferenceXy.DieCenter)
        self.mock_comm.send.assert_called_with("map:poi:reset chuck, DieCenter")

    def test_step_by_index(self):
        self.mock_comm.read_line.return_value = "0,0,0,1,2"
        result = self.prober.map.poi.step(2)
        self.mock_comm.send.assert_called_with("map:poi:step 2")
        self.assertEqual(result, (0, 1, 2))

    def test_step_by_id(self):
        self.mock_comm.read_line.return_value = "0,0,4,3,6"
        result = self.prober.map.poi.step("POI_ID")
        self.mock_comm.send.assert_called_with("map:poi:step POI_ID")
        self.assertEqual(result, (4, 3, 6))

    def test_step_first(self):
        self.mock_comm.read_line.return_value = "0,0,2,1,5"
        result = self.prober.map.poi.step_first()
        self.mock_comm.send.assert_called_with("map:poi:step_first")
        self.assertEqual(result, (2, 1, 5))

    def test_step_next(self):
        self.mock_comm.read_line.return_value = "0,0,-1,-9,0"
        result = self.prober.map.poi.step_next()
        self.mock_comm.send.assert_called_with("map:poi:step_next")
        self.assertEqual(result, (-1, -9, 0))

    def test_remove_all(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.poi.remove()
        self.mock_comm.send.assert_called_with("map:poi:remove")

    def test_remove_by_index(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.poi.remove(3)
        self.mock_comm.send.assert_called_with("map:poi:remove 3")


if __name__ == "__main__":
    unittest.main()
