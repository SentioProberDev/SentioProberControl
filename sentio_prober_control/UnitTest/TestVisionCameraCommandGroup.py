import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Enumerations import CameraMountPoint, AutoFocusAlgorithm


class TestVisionCameraCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock()
        self.prober = SentioProber(self.mock_comm)

    def test_set_light(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.camera.set_light(CameraMountPoint.Scope, 80)
        self.mock_comm.send.assert_called_with("vis:set_prop light, scope, 80")

    def test_set_exposure(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.camera.set_exposure(CameraMountPoint.Scope, 2000)
        self.mock_comm.send.assert_called_with("vis:set_prop exposure, scope, 2000")

    def test_set_gain(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.camera.set_gain(CameraMountPoint.Scope, 1.5)
        self.mock_comm.send.assert_called_with("vis:set_prop gain, scope, 1.5")

    def test_get_light(self):
        self.mock_comm.read_line.return_value = "0,0,90"
        result = self.prober.vision.camera.get_light(CameraMountPoint.Scope)
        self.mock_comm.send.assert_called_with("vis:get_prop light, scope")
        self.assertEqual(result, 90.0)

    def test_get_exposure(self):
        self.mock_comm.read_line.return_value = "0,0,2500"
        result = self.prober.vision.camera.get_exposure(CameraMountPoint.Scope)
        self.mock_comm.send.assert_called_with("vis:get_prop exposure, scope")
        self.assertEqual(result, 2500.0)

    def test_get_focus_value(self):
        self.mock_comm.read_line.return_value = "0,0,35"
        result = self.prober.vision.camera.get_focus_value(CameraMountPoint.Scope, AutoFocusAlgorithm.Bandpass)
        self.mock_comm.send.assert_called_with("vis:get_focus_value scope, Bandpass")
        self.assertEqual(result, 35.0)

    def test_get_gain(self):
        self.mock_comm.read_line.return_value = "0,0,2.3"
        result = self.prober.vision.camera.get_gain(CameraMountPoint.Scope)
        self.mock_comm.send.assert_called_with("vis:get_prop gain, scope")
        self.assertEqual(result, 2.3)

    def test_get_calib(self):
        self.mock_comm.read_line.return_value = "0,0,0.12,0.15"
        result = self.prober.vision.camera.get_calib(CameraMountPoint.Scope)
        self.mock_comm.send.assert_called_with("vis:get_prop calib, scope")
        self.assertEqual(result, (0.12, 0.15))

    def test_get_image_size(self):
        self.mock_comm.read_line.return_value = "0,0,1920,1080"
        result = self.prober.vision.camera.get_image_size(CameraMountPoint.Scope)
        self.mock_comm.send.assert_called_with("vis:get_prop image_size, scope")
        self.assertEqual(result, (1920, 1080))

    def test_is_pattern_trained_true(self):
        self.mock_comm.read_line.return_value = "0,0,1"
        result = self.prober.vision.camera.is_pattern_trained(CameraMountPoint.Scope, "MyPattern")
        self.mock_comm.send.assert_called_with("vis:pattern:is_trained scope, MyPattern")
        self.assertTrue(result)

    def test_is_pattern_trained_false(self):
        self.mock_comm.read_line.return_value = "0,0,0"
        result = self.prober.vision.camera.is_pattern_trained(CameraMountPoint.Scope, "NotTrained")
        self.mock_comm.send.assert_called_with("vis:pattern:is_trained scope, NotTrained")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
