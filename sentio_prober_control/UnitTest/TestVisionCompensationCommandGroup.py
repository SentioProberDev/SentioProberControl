import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Sentio.Enumerations import CompensationMode, CompensationType


class TestVisionCompensationGroup(unittest.TestCase):

    def setUp(self):
        self.mock_comm = MagicMock()
        self.prober = SentioProber(self.mock_comm)

    def test_enable_compensation(self):
        self.mock_comm.read_line.return_value = "0,0,Lateral,Vertical"
        result = self.prober.vision.compensation.enable(CompensationMode.Lateral, True)
        self.mock_comm.send.assert_called_with("vis:compensation:enable Lateral, True")
        self.assertEqual(result, ("Lateral", "Vertical"))

    def test_set_compensation_deprecated(self):
        self.mock_comm.read_line.return_value = "0,0,Off,On"
        result = self.prober.vision.compensation.set_compensation(CompensationMode.Vertical, False)
        self.mock_comm.send.assert_called_with("vis:compensation:enable Vertical, False")
        self.assertEqual(result, ("Off", "On"))

    def test_start_execute_compensation(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.prober.vision.compensation.start_execute(CompensationType.Topography, CompensationMode.Vertical)
        self.mock_comm.send.assert_called_with("vis:compensation:start_execute Topography, Vertical")
        self.assertTrue(resp.ok())
        self.assertEqual(resp.message(), "OK")


if __name__ == "__main__":
    unittest.main()
