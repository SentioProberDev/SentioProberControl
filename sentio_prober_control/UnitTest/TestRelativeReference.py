import unittest
from unittest.mock import MagicMock

from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Compatibility import Compatibility, CompatibilityLevel
from sentio_prober_control.Sentio.Enumerations import ProbePosition, ThetaReference, XyReference, ZReference
from sentio_prober_control.Sentio.ProberSentio import SentioProber


class TestRelativeReferenceNames(unittest.TestCase):
    """The reference to the current position is called "Relative"; "Current" is the former name."""

    RELATIVE_SPELLINGS = ("r", "R", "relative", "Relative", "current", "Current")

    def test_current_is_an_alias_of_relative(self):
        self.assertIs(XyReference.Current, XyReference.Relative)
        self.assertIs(ZReference.Current, ZReference.Relative)
        self.assertIs(ThetaReference.Current, ThetaReference.Relative)

    def test_xy_reference_reads_all_spellings(self):
        for text in self.RELATIVE_SPELLINGS:
            self.assertEqual(XyReference.from_string(text), XyReference.Relative)

    def test_z_reference_reads_all_spellings(self):
        for text in self.RELATIVE_SPELLINGS:
            self.assertEqual(ZReference.from_string(text), ZReference.Relative)

    def test_z_reference_reads_short_forms(self):
        self.assertEqual(ZReference.from_string("C"), ZReference.Contact)
        self.assertEqual(ZReference.from_string("S"), ZReference.Separation)
        self.assertEqual(ZReference.from_string("H"), ZReference.Hover)
        self.assertEqual(ZReference.from_string("Z"), ZReference.Zero)

    def test_xy_reference_reads_user(self):
        self.assertEqual(XyReference.from_string("user"), XyReference.UserDefined)


class TestRelativeReferenceIsSentAsSentioExpectsIt(unittest.TestCase):
    """A relative reference is sent with the words every SENTIO version understands, never as "Relative"."""

    ALL_LEVELS = (CompatibilityLevel.Sentio_24_0, CompatibilityLevel.Sentio_25_2, CompatibilityLevel.Sentio_26_2)

    def tearDown(self):
        Compatibility.level = CompatibilityLevel.Auto

    def _prober(self, level: CompatibilityLevel):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        prober = SentioProber(self.mock_comm, level)
        self.mock_comm.reset_mock()
        return prober

    def _sent(self) -> str:
        return self.mock_comm.send.call_args.args[0]

    def test_legacy_z_commands_send_the_short_form_in_every_version(self):
        # SENTIO up to 26.x reads only the first letter in these commands: "Current" would mean contact.
        for level in self.ALL_LEVELS:
            prober = self._prober(level)
            self.mock_comm.read_line.return_value = "0,0,100.0"

            prober.move_chuck_z(ZReference.Relative, -50)
            self.assertEqual(self._sent(), "move_chuck_z R, -50")

            prober.move_chuck_z(ZReference.Current, -50)
            self.assertEqual(self._sent(), "move_chuck_z R, -50")

            prober.move_chuck_z(ZReference.Contact, -50)
            self.assertEqual(self._sent(), "move_chuck_z C, -50")

            prober.move_scope_z(ZReference.Relative, 100)
            self.assertEqual(self._sent(), "move_scope_z R, 100")

    def test_legacy_xy_commands(self):
        for level in self.ALL_LEVELS:
            prober = self._prober(level)
            self.mock_comm.read_line.return_value = "0,0,10.0,20.0"
            prober.move_chuck_xy(XyReference.Relative, 10, 20)
            self.assertEqual(self._sent(), "move_chuck_xy R, 10, 20")

    def test_positioner_commands_send_the_long_form(self):
        # move_positioner_xy / move_positioner_z of old SENTIO versions only know the long form "Current".
        for level in self.ALL_LEVELS:
            prober = self._prober(level)

            self.mock_comm.read_line.return_value = "0,0,1.0,2.0"
            prober.probe.move_probe_xy(ProbePosition.East, XyReference.Relative, 1, 2)
            self.assertEqual(self._sent(), "move_positioner_xy East,Current,1,2")

            self.mock_comm.read_line.return_value = "0,0,3.0"
            prober.probe.move_probe_z(ProbePosition.East, ZReference.Relative, 3)
            self.assertEqual(self._sent(), "move_positioner_z East,Current,3")

    def test_generic_stage_commands(self):
        for level in (CompatibilityLevel.Sentio_25_2, CompatibilityLevel.Sentio_26_2):
            prober = self._prober(level)

            self.mock_comm.read_line.return_value = "0,0,10.0,20.0,Current"
            prober.chuck.move_xy(XyReference.Relative, 10, 20)
            self.assertEqual(self._sent(), "chuck:move_xy R,10,20")

            self.mock_comm.read_line.return_value = "0,0,5.0,Current"
            prober.chuck.move_z(ZReference.Relative, 5)
            self.assertEqual(self._sent(), "chuck:move_z Current,5")

    def test_relative_is_never_sent(self):
        # Not every SENTIO version contains the fix for #20929; "Relative" is misread by some of them.
        for level in self.ALL_LEVELS:
            for text in (XyReference.Relative.to_string(), XyReference.Relative.to_long_string(),
                         ZReference.Relative.to_string(level), ZReference.Relative.to_short_string()):
                self.assertNotEqual(text, "Relative")


class TestRelativeReferenceInResponses(unittest.TestCase):
    """SENTIO answers "Relative"; versions before the change answer "Current". Both must be read."""

    def setUp(self):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        self.prober = SentioProber(self.mock_comm, CompatibilityLevel.Sentio_26_2)
        self.mock_comm.reset_mock()

    def tearDown(self):
        Compatibility.level = CompatibilityLevel.Auto

    def test_move_z_reads_both_names(self):
        for word in ("Relative", "Current"):
            self.mock_comm.read_line.return_value = f"0,0,5.0,{word}"
            self.assertEqual(self.prober.chuck.move_z(ZReference.Relative, 5), (5.0, ZReference.Relative))

    def test_get_z_reads_both_names(self):
        for word in ("Relative", "Current"):
            self.mock_comm.read_line.return_value = f"0,0,0.0,{word}"
            self.assertEqual(self.prober.chuck.get_z(ZReference.Relative), (0.0, ZReference.Relative))

    def test_move_xy_reads_both_names(self):
        for word in ("Relative", "Current"):
            self.mock_comm.read_line.return_value = f"0,0,1.0,2.0,{word}"
            self.assertEqual(self.prober.chuck.move_xy(XyReference.Relative, 1, 2), (1.0, 2.0, XyReference.Relative))


if __name__ == "__main__":
    unittest.main()
