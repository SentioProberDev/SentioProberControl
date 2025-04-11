import unittest
from unittest.mock import MagicMock, patch
from sentio_prober_control.Sentio.CommandGroups.SetupCommandGroup import SetupCommandGroup

class TestSetupCommandGroup(unittest.TestCase):
    def setUp(self):
        self.mock_parent = MagicMock()
        self.mock_comm = MagicMock()
        self.mock_parent.comm = self.mock_comm
        self.setup = SetupCommandGroup(self.mock_parent)

    def test_get_contact_counter(self):
        self.mock_comm.read_line.return_value = "0,0,123"
        resp = self.setup.get_contact_counter()
        self.mock_comm.send.assert_called_with("setup:contact_counter:get")
        self.assertEqual(resp, 123)

    def test_reset_contact_counter(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.setup.reset_contact_counter()
        self.mock_comm.send.assert_called_with("setup:contact_counter:reset")

    def test_remote_light_off_at_contact(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.setup.remote_light_off_at_contact(True)
        self.mock_comm.send.assert_called_with("setup:remote:light_off_at_contact True")
        self.assertEqual(resp, "OK")

    def test_remote_light_on_at_separation(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.setup.remote_light_on_at_separation(False)
        self.mock_comm.send.assert_called_with("setup:remote:light_on_at_separation False")
        self.assertEqual(resp, "OK")

    def test_remote_scope_follow_off(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        resp = self.setup.remote_scope_follow_off(True)
        self.mock_comm.send.assert_called_with("setup:remote:scope_follow_off True")
        self.assertEqual(resp, "OK")

if __name__ == "__main__":
    unittest.main()