import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase
from sentio_prober_control.Sentio.Enumerations import ExecuteAction, XyCompensationType, ZCompensationType
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.WafermapCompensationCommandGroup import WafermapCompensationCommandGroup
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber


class TestWafermapCompensationCommandGroup(unittest.TestCase):
    def setUp(self):
        # Mock the TCP/IP communicator
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)

        # Create a test prober instance with the mocked communicator
        self.test_prober = SentioProber(self.mock_comm)

    def test_topography(self):
        """Test executing topography compensation"""
        self.mock_comm.read_line.return_value = "0,100,OK"
        resp = self.test_prober.map.compensation.topography(ExecuteAction.Execute)
        self.mock_comm.send.assert_called_with("map:compensation:topography execute")
        self.assertEqual(resp.cmd_id(), 100)
        self.assertEqual(resp.message(), "OK")

    def test_set_xy_compensation(self):
        """Test enabling XY compensation"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.map.compensation.set_xy(XyCompensationType.OnTheFly)
        self.mock_comm.send.assert_called_with("map:compensation:set_xy OnTheFly")

    def test_set_z_compensation(self):
        """Test enabling Z compensation"""
        self.mock_comm.read_line.return_value = "0,100,OK"
        resp = self.test_prober.map.compensation.set_z(ZCompensationType.Topography)
        self.mock_comm.send.assert_called_with("map:compensation:set_z Topography")
        self.assertEqual(resp.cmd_id(), 100)
        self.assertEqual(resp.message(), "OK")


if __name__ == "__main__":
    unittest.main()
