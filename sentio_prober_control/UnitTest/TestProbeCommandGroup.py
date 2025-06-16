import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Sentio.Enumerations import ProbePosition, ProbeXYReference, ProbeZReference
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber
class TestProbeCommandGroup(unittest.TestCase):
    def setUp(self):
        # Mock the concrete TCP/IP communicator instead of CommunicatorBase
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)

        # Ensure the mock provides `send` and `read_line` methods
        self.test_prober = SentioProber(self.mock_comm)
    def test_async_step_probe_site(self):
        self.mock_comm.read_line.return_value = "0,123,OK"
        cmd_id = self.test_prober.probe.async_step_probe_site(ProbePosition.East, 1)
        self.mock_comm.send.assert_called_with("start_step_positioner_site East,1")
        self.assertEqual(cmd_id, 123)

    def test_get_probe_site(self):
        self.mock_comm.read_line.return_value = "0,0,site1,1000,2000,Home"
        result = self.test_prober.probe.get_probe_site(ProbePosition.East, 0)
        self.mock_comm.send.assert_called_with("get_positioner_site East,0")
        self.assertEqual(result, ("site1", 1000.0, 2000.0, "Home"))

    def test_get_probe_xy(self):
        self.mock_comm.read_line.return_value = "0,0,1500,2500"
        result = self.test_prober.probe.get_probe_xy(ProbePosition.West, ProbeXYReference.Current)
        self.mock_comm.send.assert_called_with("get_positioner_xy West,Current")
        self.assertEqual(result, (1500.0, 2500.0))
    #
    def test_get_probe_z(self):
        self.mock_comm.read_line.return_value = "0,0,500"
        result = self.test_prober.probe.get_probe_z(ProbePosition.North, ProbeZReference.Zero)
        self.mock_comm.send.assert_called_with("get_positioner_z North,Zero")
        self.assertEqual(result, 500.0)

    # ---missing the relative---
    def test_move_probe_xy(self):
        self.mock_comm.read_line.return_value = "0,0,3000,4000"
        result = self.test_prober.probe.move_probe_xy(ProbePosition.South, ProbeXYReference.Home, 3000, 4000)
        self.mock_comm.send.assert_called_with("move_positioner_xy South,Home,3000,4000")
        self.assertEqual(result, (3000.0, 4000.0))

    def test_move_probe_z(self):
        self.mock_comm.read_line.return_value = "0,0,1200"
        result = self.test_prober.probe.move_probe_z(ProbePosition.West, ProbeZReference.Contact, 1200)
        self.mock_comm.send.assert_called_with("move_positioner_z West,Contact,1200")
        self.assertEqual(result, 1200.0)


if __name__ == "__main__":
    unittest.main()
