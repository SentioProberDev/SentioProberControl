import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Enumerations import AxisOrient, ColorScheme, DieNumber, RoutingStartPoint, \
    RoutingPriority, OrientationMarker


class TestWafermapCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.prober = SentioProber(self.mock_comm)

    def test_bin_step_next_die(self):
        self.mock_comm.read_line.return_value = "0,0,10,20,0"
        result = self.prober.map.bin_step_next_die(1)
        self.mock_comm.send.assert_called_with("map:bin_step_next_die 1")
        self.assertEqual(result, (10, 20, 0))

    def test_create(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.create(200.0)
        self.mock_comm.send.assert_called_with("map:create 200.0")

    def test_create_rect(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.create_rect(10, 20)
        self.mock_comm.send.assert_called_with("map:create_rect 10, 20")

    def test_die_reference_is_set(self):
        self.mock_comm.read_line.return_value = "0,0,true"
        result = self.prober.map.die_reference_is_set()
        self.mock_comm.send.assert_called_with("map:get_prop die_reference_is_set")
        self.assertTrue(result)

    def test_get_axis_orient(self):
        self.mock_comm.read_line.return_value = "0,0,UL"
        result = self.prober.map.get_axis_orient()
        self.mock_comm.send.assert_called_with("map:get_axis_orient")
        self.assertEqual(result.name, "UpLeft")

    def test_get_diameter(self):
        self.mock_comm.read_line.return_value = "0,0,200"
        result = self.prober.map.get_diameter()
        self.mock_comm.send.assert_called_with("map:get_diameter")
        self.assertEqual(result, 200)

    def test_get_die_reference(self):
        self.mock_comm.read_line.return_value = "0,0,123.45,678.90"
        result = self.prober.map.get_die_reference()
        self.mock_comm.send.assert_called_with("map:get_prop die_reference")
        self.assertEqual(result, (123.45, 678.9))

    def test_get_die_seq(self):
        self.mock_comm.read_line.return_value = "0,0,12"
        result = self.prober.map.get_die_seq()
        self.mock_comm.send.assert_called_with("map:get_die_seq")
        self.assertEqual(result, 12)

    def test_get_grid_origin(self):
        self.mock_comm.read_line.return_value = "0,0,3,5"
        result = self.prober.map.get_grid_origin()
        self.mock_comm.send.assert_called_with("map:get_grid_origin")
        self.assertEqual(result, (3, 5))

    def test_get_index_size(self):
        self.mock_comm.read_line.return_value = "0,0,5000.0,5000.0"
        result = self.prober.map.get_index_size()
        self.mock_comm.send.assert_called_with("map:get_index_size")
        self.assertEqual(result, (5000.0, 5000.0))

    def test_get_num_dies(self):
        self.mock_comm.read_line.return_value = "0,0,150"
        result = self.prober.map.get_num_dies(DieNumber.Present)
        self.mock_comm.send.assert_called_with("map:get_num_dies Present")
        self.assertEqual(result, 150)

    def test_get_street_size(self):
        self.mock_comm.read_line.return_value = "0,0,100,100"
        result = self.prober.map.get_street_size()
        self.mock_comm.send.assert_called_with("map:get_street_size")
        self.assertEqual(result, (100, 100))

    def test_get_grid_params(self):
        self.mock_comm.read_line.return_value = "0,0,5000,5000,2500,2500,1000"
        result = self.prober.map.get_grid_params()
        self.mock_comm.send.assert_called_with("map:get_grid_params")
        self.assertEqual(result, (5000.0, 5000.0, 2500.0, 2500.0, 1000.0))

    def test_get_home_die(self):
        self.mock_comm.read_line.return_value = "0,0,5,7"
        result = self.prober.map.get_home_die()
        self.mock_comm.send.assert_called_with("map:get_home_die")
        self.assertEqual(result, (5, 7))

    def test_get_num_cols(self):
        self.mock_comm.read_line.return_value = "0,0,15"
        result = self.prober.map.get_num_cols()
        self.mock_comm.send.assert_called_with("map:get_num_cols")
        self.assertEqual(result, 15)

    def test_get_num_rows(self):
        self.mock_comm.read_line.return_value = "0,0,20"
        result = self.prober.map.get_num_rows()
        self.mock_comm.send.assert_called_with("map:get_num_rows")
        self.assertEqual(result, 20)

    def test_set_axis_orient(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_axis_orient(AxisOrient.UpRight)
        self.mock_comm.send.assert_called_with("map:set_axis_orient UR")

    def test_set_color_scheme(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_color_scheme(ColorScheme.ColorFromBin)
        self.mock_comm.send.assert_called_with("map:set_color_scheme 0")

    def test_set_flat_params(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_flat_params(180, 15000)
        self.mock_comm.send.assert_called_with("map:set_flat_params 180, 15000")

    def test_set_grid_origin(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_grid_origin(3, 4)
        self.mock_comm.send.assert_called_with("map:set_grid_origin 3, 4")

    def test_set_grid_params(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_grid_params(5000, 5000, 2500, 2500, 1000)
        self.mock_comm.send.assert_called_with("map:set_grid_params 5000, 5000, 2500, 2500, 1000")

    def test_set_home_die(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_home_die(5, 6)
        self.mock_comm.send.assert_called_with("map:set_home_die 5, 6")

    def test_set_index_size(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_index_size(5000, 5000)
        self.mock_comm.send.assert_called_with("map:set_index_size 5000, 5000")

    def test_set_street_size(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_street_size(100, 100)
        self.mock_comm.send.assert_called_with("map:set_street_size 100, 100")

    def test_step_die(self):
        self.mock_comm.read_line.return_value = "0,0,3,4,0"
        result = self.prober.map.step_die(3, 4)
        self.mock_comm.send.assert_called_with("map:step_die 3, 4, 0")
        self.assertEqual(result, (3, 4, 0))

    def test_step_die_seq(self):
        self.mock_comm.read_line.return_value = "0,0,5,6,0"
        result = self.prober.map.step_die_seq(10, 0)
        self.mock_comm.send.assert_called_with("map:step_die_seq 10, 0")
        self.assertEqual(result, (5, 6, 0))

    def test_step_first_die(self):
        self.mock_comm.read_line.return_value = "0,0,1,2,0"
        result = self.prober.map.step_first_die()
        self.mock_comm.send.assert_called_with("map:step_first_die")
        self.assertEqual(result, (1, 2, 0))

    def test_step_next_die(self):
        self.mock_comm.read_line.return_value = "0,0,2,3,0"
        result = self.prober.map.step_next_die()
        self.mock_comm.send.assert_called_with("map:step_next_die")
        self.assertEqual(result, (2, 3, 0))

    def test_step_previous_die(self):
        self.mock_comm.read_line.return_value = "0,0,4,5,0"
        result = self.prober.map.step_previous_die()
        self.mock_comm.send.assert_called_with("map:step_previous_die")
        self.assertEqual(result, (4, 5, 0))

    def test_end_of_route_flag(self):
        # 手動設置 _WafermapCommandGroup__end_of_route 為 True 測試回傳
        self.prober.map._WafermapCommandGroup__end_of_route = True
        self.assertTrue(self.prober.map.end_of_route())

    def test_open(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.open("C:/path/to/mapfile.xwmf")
        self.mock_comm.send.assert_called_with("map:open C:/path/to/mapfile.xwmf")

    def test_save(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.save("C:/path/to/output_map.xwmf")
        self.mock_comm.send.assert_called_with("map:save C:/path/to/output_map.xwmf")

    def test_set_diameter(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_diameter(200)
        self.mock_comm.send.assert_called_with("map:set_diameter 200")

    def test_get_orient_marker(self):
        self.mock_comm.read_line.return_value = "0,0,Flat,90.0,1200.0"
        marker = self.prober.map.get_orient_marker()
        self.mock_comm.send.assert_called_with("map:get_orient_marker")
        self.assertEqual(marker, (OrientationMarker.Flat, 90.0, 1200.0))

    def test_set_orient_marker(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.set_orient_marker("Notch", 180.0, 600.0)
        self.mock_comm.send.assert_called_with("map:set_orient_marker Notch,180.0,600.0")

    def test_get_routing(self):
        self.mock_comm.read_line.return_value = "0,0,UL,R"
        routing = self.prober.map.get_routing()
        self.mock_comm.send.assert_called_with("map:get_routing")
        self.assertEqual(routing[0].name, RoutingStartPoint.UpperLeft)
        self.assertEqual(routing[1].name, RoutingPriority.RowUniDir)


if __name__ == "__main__":
    unittest.main()
