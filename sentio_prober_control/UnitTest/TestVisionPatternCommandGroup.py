import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.Enumerations import CameraMountPoint, FindPatternReference, DefaultPattern
from sentio_prober_control.Sentio.ProberSentio import SentioProber


class TestPatternCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock()
        self.prober = SentioProber(self.mock_comm)

    def test_find_pattern(self):
        self.mock_comm.read_line.return_value = "0,0,85.2,120.0,-30.5,1.0"
        result = self.prober.vision.pattern.find("MyPattern", threshold=85, pattern_index=1,
                                                 reference=FindPatternReference.CenterOfRoi)
        self.mock_comm.send.assert_called_with("vis:find_pattern MyPattern, 85, 1, CenterOfRoi")
        self.assertEqual(result, (85.2, 120.0, -30.5, 1.0))

    def test_get_chuck_pos(self):
        self.mock_comm.read_line.return_value = "0,0,100.0,200.0"
        result = self.prober.vision.pattern.get_chuck_pos(CameraMountPoint.Scope, DefaultPattern.DieAlignPos1)
        self.mock_comm.send.assert_called_with("vis:pattern:get_chuck_pos scope, diealignpos1")
        self.assertEqual(result, (100.0, 200.0))

    def test_set_chuck_pos(self):
        self.mock_comm.read_line.return_value = "0,0,100.0,200.0"
        result = self.prober.vision.pattern.set_chuck_pos(CameraMountPoint.Scope, DefaultPattern.TwoPoint, 100.0, 200.0)
        self.mock_comm.send.assert_called_with("vis:pattern:set_chuck_pos scope, 2pt, 100.0, 200.0")
        self.assertEqual(result, (100.0, 200.0))

    def test_show_training_box(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.pattern.show_training_box(True)
        self.mock_comm.send.assert_called_with("vis:pattern:show_training_box true")

    def test_train(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.vision.pattern.train("MyPattern")
        self.mock_comm.send.assert_called_with("vis:pattern:train MyPattern")


if __name__ == "__main__":
    unittest.main()
