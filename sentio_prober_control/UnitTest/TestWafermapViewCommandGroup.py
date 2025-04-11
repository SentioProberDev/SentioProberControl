import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber


class TestWafermapViewCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.prober = SentioProber(self.mock_comm)

    def test_show_current_die(self):
        """Test map:view:show_current_die command"""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.prober.map.view.show_current_die()
        self.mock_comm.send.assert_called_with("map:view:show_current_die")


if __name__ == "__main__":
    unittest.main()
