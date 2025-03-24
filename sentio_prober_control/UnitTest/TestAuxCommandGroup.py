import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Sentio.Response import Response

# A FakeResponse class that strips the "0,0," prefix from the response.
class FakeResponse:
    def __init__(self, message):
        self._message = message

    def message(self):
        prefix = "0,0,"
        if self._message.startswith(prefix):
            return self._message[len(prefix):]
        return self._message

# Save the original Response.check_resp so we can restore it after tests.
_original_check_resp = Response.check_resp
# Patch Response.check_resp to wrap the raw line in a FakeResponse.
Response.check_resp = lambda line: FakeResponse(line)

class TestAuxCommandGroup(unittest.TestCase):
    def setUp(self):
        # Create a mock communicator based on CommunicatorTcpIp.
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)
        # Create a SentioProber instance (which instantiates the aux command group).
        self.prober = SentioProber(self.mock_comm)
        self.aux = self.prober.aux

    def tearDown(self):
        # Restore the original Response.check_resp.
        Response.check_resp = _original_check_resp

    # 1) Test retrieve_substrate_data
    def test_retrieve_substrate_data_no_site(self):
        self.mock_comm.read_line.return_value = "0,0,3,Aux1,Aux2,Aux3"
        count, sites = self.aux.retrieve_substrate_data()
        self.mock_comm.send.assert_called_with("aux:retrieve_substrate_data")
        self.assertEqual(count, 3)
        self.assertEqual(sites, ["Aux1", "Aux2", "Aux3"])

    def test_retrieve_substrate_data_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,1,Aux1"
        count, sites = self.aux.retrieve_substrate_data("AuxRight")
        self.mock_comm.send.assert_called_with("aux:retrieve_substrate_data AuxRight")
        self.assertEqual(count, 1)
        self.assertEqual(sites, ["Aux1"])

    # 2) Test get_substrate_type
    def test_get_substrate_type_no_site(self):
        self.mock_comm.read_line.return_value = "0,0,Wafer"
        result = self.aux.get_substrate_type()
        self.mock_comm.send.assert_called_with("aux:get_substrate_type")
        self.assertEqual(result, "Wafer")

    def test_get_substrate_type_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,AC-2"
        result = self.aux.get_substrate_type("0")
        self.mock_comm.send.assert_called_with("aux:get_substrate_type 0")
        self.assertEqual(result, "AC-2")

    # 3) Test step_to_element
    def test_step_to_element(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.aux.step_to_element("0102", offset_x=100.0, offset_y=200.0, motorized_positioner_move=True)
        expected_command = "aux:step_to_element 0102,100.0,200.0,true"
        self.mock_comm.send.assert_called_with(expected_command)

    # 4) Test step_to_dut_element (without and with XY coordinates)
    def test_step_to_dut_element_without_xy(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.aux.step_to_dut_element("RefDUT", move_z=False)
        expected_command = "aux:step_to_dut_element RefDUT,false"
        self.mock_comm.send.assert_called_with(expected_command)

    def test_step_to_dut_element_with_xy(self):
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.aux.step_to_dut_element("RefDUT", move_z=True, x=150100, y=149000)
        expected_command = "aux:step_to_dut_element RefDUT,true,150100,149000"
        self.mock_comm.send.assert_called_with(expected_command)

    # 5) Test get_element_type
    def test_get_element_type_without_site(self):
        self.mock_comm.read_line.return_value = "0,0,Short"
        result = self.aux.get_element_type("0102")
        expected_command = "aux:get_element_type 0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, "Short")

    def test_get_element_type_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,Thru"
        result = self.aux.get_element_type("0102", "AuxRight")
        expected_command = "aux:get_element_type AuxRight,0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, "Thru")

    # 6) Test get_substrate_info
    def test_get_substrate_info(self):
        self.mock_comm.read_line.return_value = "0,0,AC-2,ac2,4.48"
        result = self.aux.get_substrate_info("AuxLeft")
        expected_command = "aux:get_substrate_info AuxLeft"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, {"substrate_type": "AC-2", "substrate_id": "ac2", "life_time": 4.48})

    # 7) Test get_element_touch_count
    def test_get_element_touch_count_without_site(self):
        self.mock_comm.read_line.return_value = "0,0,5"
        result = self.aux.get_element_touch_count("0102")
        expected_command = "aux:get_element_touch_count 0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, 5)

    def test_get_element_touch_count_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,7"
        result = self.aux.get_element_touch_count("0102", "AuxRight")
        expected_command = "aux:get_element_touch_count AuxRight,0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, 7)

    # 8) Test get_element_spacing
    def test_get_element_spacing_without_site(self):
        self.mock_comm.read_line.return_value = "0,0,150.0"
        result = self.aux.get_element_spacing("0102")
        expected_command = "aux:get_element_spacing 0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, 150.0)

    def test_get_element_spacing_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,200.5"
        result = self.aux.get_element_spacing("0102", "AuxLeft")
        expected_command = "aux:get_element_spacing AuxLeft,0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, 200.5)

    # 9) Test get_element_pos
    def test_get_element_pos_without_site(self):
        self.mock_comm.read_line.return_value = "0,0,150.0,250.0"
        result = self.aux.get_element_pos("0102")
        expected_command = "aux:get_element_pos 0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, (150.0, 250.0))

    def test_get_element_pos_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,100.0,200.0"
        result = self.aux.get_element_pos("0102", "AuxRight")
        expected_command = "aux:get_element_pos AuxRight,0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, (100.0, 200.0))

    # 10) Test get_element_life_time
    def test_get_element_life_time_without_site(self):
        self.mock_comm.read_line.return_value = "0,0,90.0"
        result = self.aux.get_element_life_time("0102")
        expected_command = "aux:get_element_life_time 0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, 90.0)

    def test_get_element_life_time_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,85.5"
        result = self.aux.get_element_life_time("0102", "AuxLeft")
        expected_command = "aux:get_element_life_time AuxLeft,0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, 85.5)

    # 11) Test get_element_info
    def test_get_element_info_without_site(self):
        self.mock_comm.read_line.return_value = "0,0,Thru,GSG,150.0,250.0,50.0,2,95.0"
        result = self.aux.get_element_info("0102")
        expected_command = "aux:get_element_info 0102"
        self.mock_comm.send.assert_called_with(expected_command)
        expected_dict = {
            "element_type": "Thru",
            "element_subtype": "GSG",
            "x_position": 150.0,
            "y_position": 250.0,
            "spacing": 50.0,
            "touch_count": 2,
            "life_time": 95.0
        }
        self.assertEqual(result, expected_dict)

    def test_get_element_info_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,Open,NonGSG,100.0,200.0,30.0,1,99.0"
        result = self.aux.get_element_info("0102", "AuxRight")
        expected_command = "aux:get_element_info AuxRight,0102"
        self.mock_comm.send.assert_called_with(expected_command)
        expected_dict = {
            "element_type": "Open",
            "element_subtype": "NonGSG",
            "x_position": 100.0,
            "y_position": 200.0,
            "spacing": 30.0,
            "touch_count": 1,
            "life_time": 99.0
        }
        self.assertEqual(result, expected_dict)

if __name__ == "__main__":
    unittest.main()