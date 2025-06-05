import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.Enumerations import ChuckSite
from sentio_prober_control.Sentio.ProberBase import ProberException
# Import our AuxCommandGroup and related types (without SubstrateType)
from sentio_prober_control.Sentio.CommandGroups.AuxCommandGroup import (
    AuxCommandGroup,
    ElementInfo,
    ElementType,
    ElementInfoResponse,
)

# A FakeResponse class that strips the "0,0," prefix from the response.
class FakeResponse:
    def __init__(self, message: str):
        self._message = message

    def message(self) -> str:
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
        self.aux: AuxCommandGroup = self.prober.aux

    def tearDown(self):
        # Restore the original Response.check_resp.
        Response.check_resp = _original_check_resp

    # 1) Test retrieve_substrate_data
    def test_retrieve_substrate_data_no_site(self):
        # Return response with three sites: AuxRight, AuxLeft, AuxRight2
        self.mock_comm.read_line.return_value = "0,0,3,AuxRight,AuxLeft,AuxRight2"
        sites = self.aux.retrieve_substrate_data()
        self.mock_comm.send.assert_called_with("aux:retrieve_substrate_data")
        expected_sites = [ChuckSite.AuxRight, ChuckSite.AuxLeft, ChuckSite.AuxRight2]
        self.assertEqual(sites, expected_sites)

    def test_retrieve_substrate_data_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,1,AuxRight"
        sites = self.aux.retrieve_substrate_data(ChuckSite.AuxRight)
        expected_command = "aux:retrieve_substrate_data " + ChuckSite.AuxRight.to_string()
        self.mock_comm.send.assert_called_with(expected_command)
        expected_sites = [ChuckSite.AuxRight]
        self.assertEqual(sites, expected_sites)

    # 2) Test get_substrate_type
    def test_get_substrate_type_no_site(self):
        self.mock_comm.read_line.return_value = "0,0,Wafer"
        result = self.aux.get_substrate_type()
        self.mock_comm.send.assert_called_with("aux:get_substrate_type")
        self.assertEqual(result, "Wafer")

    def test_get_substrate_type_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,AC-2"
        result = self.aux.get_substrate_type(ChuckSite.AuxLeft)
        expected_command = "aux:get_substrate_type " + ChuckSite.AuxLeft.to_string()
        self.mock_comm.send.assert_called_with(expected_command)
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
        self.assertEqual(result, ElementType.Short)

    def test_get_element_type_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,Thru"
        result = self.aux.get_element_type("0102", ChuckSite.AuxRight)
        expected_command = "aux:get_element_type " + ChuckSite.AuxRight.to_string() + ",0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, ElementType.Thru)

    # 6) Test get_substrate_info
    def test_get_substrate_info(self):
        self.mock_comm.read_line.return_value = "0,0,AC-2,ac2,4.48"
        result = self.aux.get_substrate_info(ChuckSite.AuxLeft)
        expected_command = "aux:get_substrate_info " + ChuckSite.AuxLeft.to_string()
        self.mock_comm.send.assert_called_with(expected_command)
        expected = ("AC-2", "ac2", 4.48)
        self.assertEqual(result, expected)

    def test_get_substrate_info_invalid_site_wafer(self):
        with self.assertRaises(ProberException):
            self.aux.get_substrate_info(ChuckSite.Wafer)

    def test_get_substrate_info_invalid_site_chuckcamera(self):
        with self.assertRaises(ProberException):
            self.aux.get_substrate_info(ChuckSite.ChuckCamera)

    # 7) Test get_element_touch_count
    def test_get_element_touch_count_without_site(self):
        self.mock_comm.read_line.return_value = "0,0,5"
        result = self.aux.get_element_touch_count("0102")
        expected_command = "aux:get_element_touch_count 0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, 5)

    def test_get_element_touch_count_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,7"
        result = self.aux.get_element_touch_count("0102", ChuckSite.AuxRight)
        expected_command = "aux:get_element_touch_count " + ChuckSite.AuxRight.to_string() + ",0102"
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
        result = self.aux.get_element_spacing("0102", ChuckSite.AuxLeft)
        expected_command = "aux:get_element_spacing " + ChuckSite.AuxLeft.to_string() + ",0102"
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
        result = self.aux.get_element_pos("0102", ChuckSite.AuxRight)
        expected_command = "aux:get_element_pos " + ChuckSite.AuxRight.to_string() + ",0102"
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
        result = self.aux.get_element_life_time("0102", ChuckSite.AuxLeft)
        expected_command = "aux:get_element_life_time " + ChuckSite.AuxLeft.to_string() + ",0102"
        self.mock_comm.send.assert_called_with(expected_command)
        self.assertEqual(result, 85.5)

    # 11) Test get_element_info
    def test_get_element_info_without_site(self):
        # Raw response: element_type,element_subtype,x_position,y_position,spacing,touch_count,life_time
        self.mock_comm.read_line.return_value = "0,0,Thru,GSG,150.0,250.0,50.0,2,95.0"
        result = self.aux.get_element_info("0102")
        expected_command = "aux:get_element_info 0102"
        self.mock_comm.send.assert_called_with(expected_command)
        expected = ElementInfo(
            element_type=ElementType.Thru,
            element_subtype="GSG",
            x_position=150.0,
            y_position=250.0,
            spacing=50.0,
            touch_count=2,
            life_time=95.0
        )
        self.assertEqual(result, expected)

    def test_get_element_info_with_site(self):
        self.mock_comm.read_line.return_value = "0,0,Open,NonGSG,100.0,200.0,30.0,1,99.0"
        result = self.aux.get_element_info("0102", ChuckSite.AuxRight)
        expected_command = "aux:get_element_info " + ChuckSite.AuxRight.to_string() + ",0102"
        self.mock_comm.send.assert_called_with(expected_command)
        expected = ElementInfo(
            element_type=ElementType.Open,
            element_subtype="NonGSG",
            x_position=100.0,
            y_position=200.0,
            spacing=30.0,
            touch_count=1,
            life_time=99.0
        )
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
