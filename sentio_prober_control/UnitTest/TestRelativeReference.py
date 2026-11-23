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

    def test_to_string_is_the_only_conversion_to_text(self):
        # One conversion per enum, controlled by the compatibility level. A second one (to_short_string,
        # to_long_string, ...) lets every command pick its own spelling again.
        for enum_type in (XyReference, ZReference, ThetaReference):
            conversions = [name for name in vars(enum_type) if name.startswith("to_")]
            self.assertEqual(conversions, ["to_string"], enum_type.__name__)


class TestRelativeReferenceIsSentAsSentioExpectsIt(unittest.TestCase):
    """What is sent for a relative reference depends on the SENTIO version; it must work with every version.

        before 25.2:   short form "R"; the positioner commands need the enum name "Current"
        25.2 and 25.3: long form, but "R" for the relative reference ("Relative" is not known yet and "Current"
                       is read as contact by the commands that only evaluate the first letter)
        from 26.0:     long form, "Relative"
    """

    BEFORE_25_2 = CompatibilityLevel.Sentio_24_0, CompatibilityLevel.Sentio_25_1
    FROM_26_0 = CompatibilityLevel.Sentio_26_0, CompatibilityLevel.Sentio_26_2

    def tearDown(self):
        Compatibility.level = CompatibilityLevel.Auto

    def _prober(self, level: CompatibilityLevel):
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        prober = SentioProber(self.mock_comm, level)
        self.mock_comm.reset_mock()
        return prober

    def _sent(self) -> str:
        return self.mock_comm.send.call_args.args[0]

    def _words(self, before_25_2: str, sentio_25_2: str, from_26_0: str) -> dict:
        words = {level: before_25_2 for level in self.BEFORE_25_2}
        words[CompatibilityLevel.Sentio_25_2] = sentio_25_2
        words.update({level: from_26_0 for level in self.FROM_26_0})
        return words

    def test_legacy_z_commands(self):
        relative = self._words("R", "R", "Relative")
        contact = self._words("C", "Contact", "Contact")
        for level in relative:
            prober = self._prober(level)
            self.mock_comm.read_line.return_value = "0,0,100.0"

            prober.move_chuck_z(ZReference.Relative, -50)
            self.assertEqual(self._sent(), f"move_chuck_z {relative[level]}, -50")

            prober.move_chuck_z(ZReference.Current, -50)
            self.assertEqual(self._sent(), f"move_chuck_z {relative[level]}, -50")

            prober.move_chuck_z(ZReference.Contact, -50)
            self.assertEqual(self._sent(), f"move_chuck_z {contact[level]}, -50")

            prober.get_chuck_z(ZReference.Relative)
            self.assertEqual(self._sent(), f"get_chuck_z {relative[level]}")

            prober.move_scope_z(ZReference.Relative, 100)
            self.assertEqual(self._sent(), f"move_scope_z {relative[level]}, 100")

    def test_legacy_xy_commands(self):
        relative = self._words("R", "R", "Relative")
        zero = self._words("Z", "Zero", "Zero")
        for level in relative:
            prober = self._prober(level)
            self.mock_comm.read_line.return_value = "0,0,10.0,20.0"

            prober.move_chuck_xy(XyReference.Relative, 10, 20)
            self.assertEqual(self._sent(), f"move_chuck_xy {relative[level]}, 10, 20")

            prober.move_chuck_xy(XyReference.Zero, 10, 20)
            self.assertEqual(self._sent(), f"move_chuck_xy {zero[level]}, 10, 20")

    def test_positioner_commands(self):
        # SENTIO before 25.2 reads the reference of these commands by its enum name.
        relative = self._words("Current", "R", "Relative")
        for level in relative:
            prober = self._prober(level)

            self.mock_comm.read_line.return_value = "0,0,1.0,2.0"
            prober.probe.move_probe_xy(ProbePosition.East, XyReference.Relative, 1, 2)
            self.assertEqual(self._sent(), f"move_positioner_xy East,{relative[level]},1,2")

            prober.probe.get_probe_xy(ProbePosition.East, XyReference.Zero)
            self.assertEqual(self._sent(), "get_positioner_xy East,Zero")

            self.mock_comm.read_line.return_value = "0,0,3.0"
            prober.probe.move_probe_z(ProbePosition.East, ZReference.Relative, 3)
            self.assertEqual(self._sent(), f"move_positioner_z East,{relative[level]},3")

            prober.probe.get_probe_z(ProbePosition.East, ZReference.Contact)
            self.assertEqual(self._sent(), "get_positioner_z East,Contact")

    def test_generic_stage_commands(self):
        relative = {
            CompatibilityLevel.Sentio_25_2: "R",
            CompatibilityLevel.Sentio_26_0: "Relative",
            CompatibilityLevel.Sentio_26_2: "Relative",
        }
        for level, word in relative.items():
            prober = self._prober(level)

            self.mock_comm.read_line.return_value = "0,0,10.0,20.0,Current"
            prober.chuck.move_xy(XyReference.Relative, 10, 20)
            self.assertEqual(self._sent(), f"chuck:move_xy {word},10,20")

            self.mock_comm.read_line.return_value = "0,0,5.0,Current"
            prober.chuck.move_z(ZReference.Relative, 5)
            self.assertEqual(self._sent(), f"chuck:move_z {word},5")

    def test_current_is_never_sent_to_sentio_25_2_or_newer(self):
        # move_chuck_z, get_chuck_z, move_scope_z and move_vce_z read "Current" as contact.
        for level in (CompatibilityLevel.Sentio_25_2, *self.FROM_26_0):
            self.assertNotEqual(ZReference.Relative.to_string(level), "Current")
            self.assertNotEqual(XyReference.Relative.to_string(level), "Current")

    def test_sentio_version_selects_the_level(self):
        levels = {
            "25.1.0": CompatibilityLevel.Sentio_25_1,
            "25.2.1": CompatibilityLevel.Sentio_25_2,
            "25.3.0": CompatibilityLevel.Sentio_25_2,
            "26.0.0": CompatibilityLevel.Sentio_26_0,
            "26.1.3": CompatibilityLevel.Sentio_26_0,
            "26.2.0": CompatibilityLevel.Sentio_26_2,
        }
        for version, level in levels.items():
            mock_comm = MagicMock(spec=CommunicatorTcpIp)
            mock_comm.read_line.return_value = f"0,0,Version: {version}"
            SentioProber(mock_comm, CompatibilityLevel.Auto)
            self.assertEqual(Compatibility.level, level, version)


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
