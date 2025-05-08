import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.Enumerations import AxisOrient, StatusBits
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp


class TestWafermapSubsiteGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.prober = SentioProber(self.mock_comm)

    def test_add(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.subsites.add("A", 100.0, 200.0, AxisOrient.UpLeft)
        self.mock_comm.send.assert_called_with("map:subsite:add A, 100.0, 200.0, UL")

    def test_bin_step_next(self):
        self.mock_comm.read_line.return_value = "0,0,5,6,1"
        result = self.prober.map.subsites.bin_step_next(2)
        self.mock_comm.send.assert_called_with("map:subsite:bin_step_next 2")
        self.assertEqual(result, (5, 6, 1))

    def test_get_with_orientation(self):
        self.mock_comm.read_line.return_value = "0,0,Site1,100.0,200.0"
        result = self.prober.map.subsites.get(0, AxisOrient.DownRight)
        self.mock_comm.send.assert_called_with("map:subsite:get 0, DR")
        self.assertEqual(result, ("Site1", 100.0, 200.0))

    def test_get_with_default_orientation(self):
        self.mock_comm.read_line.return_value = "0,0,SiteX,123.4,567.8"
        result = self.prober.map.subsites.get(1)
        self.mock_comm.send.assert_called_with("map:subsite:get 1, MAP")
        self.assertEqual(result, ("SiteX", 123.4, 567.8))

    def test_get_num(self):
        self.mock_comm.read_line.return_value = "0,0,4"
        result = self.prober.map.subsites.get_num()
        self.mock_comm.send.assert_called_with("map:subsite:get_num")
        self.assertEqual(result, 4)

    def test_reset(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.subsites.reset()
        self.mock_comm.send.assert_called_with("map:subsite:reset")

    def test_step_with_index(self):
        self.mock_comm.read_line.return_value = "0,0,5,10,1"
        result = self.prober.map.subsites.step(1)
        self.mock_comm.send.assert_called_with("map:subsite:step 1")
        self.assertEqual(result, (5, 10, 1))

    def test_step_with_id_string(self):
        self.mock_comm.read_line.return_value = "0,0,3,7,0"
        result = self.prober.map.subsites.step("SubA")
        self.mock_comm.send.assert_called_with("map:subsite:step SubA")
        self.assertEqual(result, (3, 7, 0))

    def test_step_next(self):
        self.mock_comm.read_line.return_value = "0,0,8,9,2"
        result = self.prober.map.subsites.step_next()
        self.mock_comm.send.assert_called_with("map:subsite:step_next")
        self.assertEqual(result, (8, 9, 2))

    def test_export(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.subsites.export("subsite_export.csv")
        self.mock_comm.send.assert_called_with("map:subsite:export subsite_export.csv")

    def test_get_state_global(self):
        self.mock_comm.read_line.return_value = "0,0,1"
        result = self.prober.map.subsites.get_state("Site1")
        self.mock_comm.send.assert_called_with("map:subsite:get_state Site1")
        self.assertEqual(result, 1)

    def test_get_state_local(self):
        self.mock_comm.read_line.return_value = "0,0,0"
        result = self.prober.map.subsites.get_state(1, 5, 6)
        self.mock_comm.send.assert_called_with("map:subsite:get_state 1, 5, 6")
        self.assertEqual(result, 0)

    def test_import_from_file(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.subsites.import_from_file("subsite_import.xlsx")
        self.mock_comm.send.assert_called_with("map:subsite:import subsite_import.xlsx")

    def test_remove(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.subsites.remove("SiteToDelete")
        self.mock_comm.send.assert_called_with("map:subsite:remove SiteToDelete")

    def test_set_state_global(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.subsites.set_state("Sub1", 1)
        self.mock_comm.send.assert_called_with("map:subsite:set_state Sub1, 1")

    def test_set_state_local(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.subsites.set_state("Sub1", 0, 2, 3)
        self.mock_comm.send.assert_called_with("map:subsite:set_state Sub1, 0, 2, 3")

    def test_step_previous(self):
        self.mock_comm.read_line.return_value = "0,0,2,3,1"
        result = self.prober.map.subsites.step_previous()
        self.mock_comm.send.assert_called_with("map:subsite:step_previous")
        self.assertEqual(result, (2, 3, 1))


if __name__ == "__main__":
    unittest.main()
