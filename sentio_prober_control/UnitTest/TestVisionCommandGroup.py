import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Enumerations import (
    CameraMountPoint,
    AutoFocusCmd,
    AutoAlignCmd,
    PtpaFindTipsMode,
    SnapshotType,
    SnapshotLocation,
    PtpaType, DieCompensationType, DieCompensationMode, MoveAxis
)


class TestVisionCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.prober = SentioProber(self.mock_comm)

    def test_align_wafer(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.align_wafer(AutoAlignCmd.UpdateDieSize)
        self.mock_comm.send.assert_called_with("vis:align_wafer update")

    def test_align_die(self):
        self.mock_comm.read_line.return_value = "0,0,10.0,20.0,0.1"
        result = self.prober.vision.align_die()
        self.mock_comm.send.assert_called_with("vis:align_die 0.05")
        self.assertEqual(result, (10.0, 20.0, 0.1))

    def test_auto_focus_default(self):
        self.mock_comm.read_line.return_value = "0,0,13500,scope"
        result = self.prober.vision.auto_focus()
        self.mock_comm.send.assert_called_with("vis:auto_focus F")
        self.assertEqual(result, (13500.0, MoveAxis.Scope))

    def test_auto_focus_parameter(self):
        self.mock_comm.read_line.return_value = "0,0,46500,chuck"
        result = self.prober.vision.auto_focus(AutoFocusCmd.GoTo)
        self.mock_comm.send.assert_called_with("vis:auto_focus G")
        self.assertEqual(result, (46500.0, MoveAxis.Chuck))

    def test_camera_synchronize(self):
        self.mock_comm.read_line.return_value = "0,0,1.1,2.2,3.3"
        result = self.prober.vision.camera_synchronize()
        self.mock_comm.send.assert_called_with("vis:camera_synchronize")
        self.assertEqual(result, (1.1, 2.2, 3.3))

    def test_find_home(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.find_home()
        self.mock_comm.send.assert_called_with("vis:find_home")

    def test_enable_follow_mode(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.enable_follow_mode(True)
        self.mock_comm.send.assert_called_with("vis:enable_follow_mode True")

    def test_switch_all_lights(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.switch_all_lights(True)
        self.mock_comm.send.assert_called_with("vis:switch_all_lights True")

    def test_detect_probetips(self):
        self.mock_comm.read_line.return_value = "0,0,100 200 10 10 0.98 1"
        result = self.prober.vision.detect_probetips(CameraMountPoint.Scope)
        self.mock_comm.send.assert_called_with("vis:detect_probetips scope, ProbeDetector, Roi")
        self.assertEqual(result[0][0:5], [100.0, 200.0, 10.0, 10.0, 0.98])

    def test_ptpa_find_tips(self):
        self.mock_comm.read_line.return_value = "0,0,100.0,200.0,300.0"
        result = self.prober.vision.ptpa_find_tips(PtpaFindTipsMode.OnAxis)
        self.mock_comm.send.assert_called_with("vis:ptpa_find_tips OnAxis")
        self.assertEqual(result, (100.0, 200.0, 300.0))

    def test_snap_image_to_prober(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.snap_image("test.jpg", SnapshotType.CameraRaw, SnapshotLocation.Prober)
        self.mock_comm.send.assert_called_with("vis:snap_image test.jpg, 0")

    def test_get_light_status(self):
        self.mock_comm.read_line.return_value = "0,0,1"
        result = self.prober.vision.get_light_status(CameraMountPoint.Scope)
        self.mock_comm.send.assert_called_with("vis:get_light_status scope")
        self.assertTrue(result)

    def test_get_lens_zoom_level(self):
        self.mock_comm.read_line.return_value = "0,0,8.0"
        result = self.prober.vision.get_lens_zoom_level()
        self.mock_comm.send.assert_called_with("vis:get_lens_zoom_level")
        self.assertEqual(result, 8.0)

    def test_set_lens_zoom_level(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.set_lens_zoom_level(6.0)
        self.mock_comm.send.assert_called_with("vis:set_lens_zoom_level 6.0")

    def test_find_thermal_die_size(self):
        self.mock_comm.read_line.return_value = "0,0,1.001,0.999"
        result = self.prober.vision.find_thermal_die_size()
        self.mock_comm.send.assert_called_with("vis:find_thermal_die_size")
        self.assertEqual(result, (1.001, 0.999))

    def test_find_pattern(self):
        self.mock_comm.read_line.return_value = "0,0,95.0,100.0,200.0,0.3"
        result = self.prober.vision.find_pattern("MyPattern", 95, 1)
        self.mock_comm.send.assert_called_with("vis:find_pattern MyPattern, 95, 1, CenterOfRoi")
        self.assertEqual(result, (95.0, 100.0, 200.0, 0.3))

    def test_has_camera_true(self):
        self.mock_comm.read_line.return_value = "0,0,1"
        result = self.prober.vision.has_camera(CameraMountPoint.Scope)
        self.mock_comm.send.assert_called_with("vis:has_camera scope")
        self.assertTrue(result)

    def test_has_camera_false(self):
        self.mock_comm.read_line.return_value = "0,0,0"
        result = self.prober.vision.has_camera(CameraMountPoint.OffAxis)
        self.mock_comm.send.assert_called_with("vis:has_camera offaxis")
        self.assertFalse(result)

    def test_remove_probetip_marker(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.remove_probetip_marker()
        self.mock_comm.send.assert_called_with("vis:remove_probetip_marker")

    def test_match_tips(self):
        self.mock_comm.read_line.return_value = "0,0,0.123,0.456"
        result = self.prober.vision.match_tips(PtpaType.OffAxis)
        self.mock_comm.send.assert_called_with("vis:match_tips offaxis")
        self.assertEqual(result, (0.123, 0.456))

    def test_switch_light(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.switch_light(CameraMountPoint.Scope, True)
        self.mock_comm.send.assert_called_with("vis:switch_light scope, True")

    def test_switch_camera(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.switch_camera(CameraMountPoint.OffAxis)
        self.mock_comm.send.assert_called_with("vis:switch_camera offaxis")

    def test_ptpa_find_pads(self):
        self.mock_comm.read_line.return_value = "0,0,10.0,20.0,30.0"
        result = self.prober.vision.ptpa_find_pads(5, 10)
        self.mock_comm.send.assert_called_with("vis:execute_ptpa_find_pads 5,10")
        self.assertEqual(result, (10.0, 20.0, 30.0))

    def test_start_fast_track(self):
        self.prober.send_cmd = MagicMock()
        self.prober.vision.start_fast_track()
        self.prober.send_cmd.assert_called_with("vis:start_fast_track")

    def test_start_execute_compensation(self):
        self.mock_comm.read_line.return_value = "0,3,OK"
        result = self.prober.vision.start_execute_compensation(
            DieCompensationType.DieAlign,
            DieCompensationMode.Lateral
        )
        self.mock_comm.send.assert_called_with("vis:compensation:start_execute DieAlign,Lateral")
        self.assertIsInstance(result.cmd_id(), int)  # cmd_id should be returned
        self.assertGreater(result.cmd_id(), 0, "cmd_id should be greater than 0")


if __name__ == "__main__":
    unittest.main()
