import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Compatibility import Compatibility, CompatibilityLevel
from sentio_prober_control.Sentio.ProberSentio import SentioProber


class TestCompatibilityLevelSelection(unittest.TestCase):
    """Tests for how SentioProber determines the compatibility level on construction."""

    def setUp(self):
        Compatibility.level = CompatibilityLevel.Auto
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)

    def tearDown(self):
        Compatibility.level = CompatibilityLevel.Auto

    def test_explicit_compat_level_is_applied(self):
        """An explicitly passed compatibility level must be used as is."""
        SentioProber(self.mock_comm, CompatibilityLevel.Sentio_25_1)
        self.assertEqual(Compatibility.level, CompatibilityLevel.Sentio_25_1)

    def test_explicit_compat_level_does_not_query_version(self):
        """With an explicit level SENTIO must not be asked for its version."""
        SentioProber(self.mock_comm, CompatibilityLevel.Sentio_26_2)
        sent = [c.args[0] for c in self.mock_comm.send.call_args_list]
        self.assertNotIn("status:get_version", sent)

    def test_auto_detects_level_from_version_string(self):
        """With CompatibilityLevel.Auto the level is derived from status:get_version."""
        self.mock_comm.read_line.return_value = "0,0,Version: 26.0.4"
        SentioProber(self.mock_comm, CompatibilityLevel.Auto)
        self.mock_comm.send.assert_any_call("status:get_version")
        self.assertEqual(Compatibility.level, CompatibilityLevel.Sentio_26_0)


if __name__ == "__main__":
    unittest.main()
