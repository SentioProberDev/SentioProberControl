import unittest
from unittest.mock import MagicMock
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Sentio.Enumerations import ProbePosition, UvwAxis, FiberType
from sentio_prober_control.Sentio.ProberSentio import SentioProber
from sentio_prober_control.Sentio.Response import Response

class TestSiPHCommandGroup(unittest.TestCase):
    def setUp(self):
        """Initialize the mock communicator and SiPHCommandGroup instance."""
        self.mock_comm = MagicMock(spec=CommunicatorTcpIp)

        # Ensure the mock provides `send` and `read_line` methods
        self.test_prober = SentioProber(self.mock_comm)

    def test_fast_alignment(self):
        """Test fast_alignment method."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.siph.fast_alignment()
        self.mock_comm.send.assert_called_with("siph:fast_alignment")

    def test_get_cap_sensor(self):
        """Test get_cap_sensor method."""
        self.mock_comm.read_line.return_value = "0,0,0.5,1.2"
        cap1, cap2 = self.test_prober.siph.get_cap_sensor()
        self.mock_comm.send.assert_called_with("siph:get_cap_sensor")
        self.assertEqual(cap1, 0.5)
        self.assertEqual(cap2, 1.2)

    def test_get_intensity(self):
        """Test get_intensity method."""
        self.mock_comm.read_line.return_value = "0,0,1.5"
        intensity = self.test_prober.siph.get_intensity(1)
        self.mock_comm.send.assert_called_with("siph:get_intensity 1")
        self.assertEqual(intensity, 1.5)

    def test_gradient_search(self):
        """Test gradient_search method."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.siph.gradient_search()
        self.mock_comm.send.assert_called_with("siph:gradient_search")

    def test_move_hover(self):
        """Test move_hover method."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.siph.move_hover(ProbePosition.East)
        self.mock_comm.send.assert_called_with("siph:move_hover East")

    def test_coupling(self):
        """Test coupling method."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.siph.coupling(ProbePosition.East, UvwAxis.V)
        self.mock_comm.send.assert_called_with("siph:coupling East,V")

    def test_get_alignment(self):
        """Test get_alignment method."""
        self.mock_comm.read_line.return_value = "0,0,true,false,true,true"
        coarse, fine, gradient, rotary = self.test_prober.siph.get_alignment(ProbePosition.West, FiberType.Single)
        self.mock_comm.send.assert_called_with("siph:get_alignment West,Single")
        self.assertTrue(coarse)
        self.assertFalse(fine)
        self.assertTrue(gradient)
        self.assertTrue(rotary)

    def test_set_origin(self):
        """Test set_origin method."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.siph.set_origin(ProbePosition.East)
        self.mock_comm.send.assert_called_with("siph:set_origin East")

    def test_move_origin(self):
        """Test move_origin method."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.siph.move_origin(ProbePosition.West)
        self.mock_comm.send.assert_called_with("siph:move_origin West")

    def test_move_position_uvw(self):
        """Test move_position_uvw method."""
        self.mock_comm.read_line.return_value = "0,0,0.2"
        position = self.test_prober.siph.move_position_uvw(ProbePosition.East, UvwAxis.U, 0.1)
        self.mock_comm.send.assert_called_with("siph:move_position_uvw East,U,0.1")
        self.assertEqual(position, 0.2)

    def test_pivot_point(self):
        """Test pivot_point method."""
        self.mock_comm.read_line.return_value = "0,0,OK"
        self.test_prober.siph.pivot_point(ProbePosition.West)
        self.mock_comm.send.assert_called_with("siph:pivot_point West")

    def test_move_nanocube_xy(self):
        """Test move_nanocube_xy method."""
        self.mock_comm.read_line.return_value = "0,0,50.000,50.000"
        x, y = self.test_prober.siph.move_nanocube_xy(ProbePosition.East, 50, 50)
        self.mock_comm.send.assert_called_with("siph:move_nanocube_xy East,50,50")
        self.assertEqual(x, 50.000)
        self.assertEqual(y, 50.000)

    def test_get_nanocube_xy(self):
        """Test get_nanocube_xy method."""
        self.mock_comm.read_line.return_value = "0,0,50.000,50.000"
        x, y = self.test_prober.siph.get_nanocube_xy(ProbePosition.East)
        self.mock_comm.send.assert_called_with("siph:get_nanocube_xy East")
        self.assertEqual(x, 50.000)
        self.assertEqual(y, 50.000)

    def test_get_nanocube_z(self):
        """Test get_nanocube_z method."""
        self.mock_comm.read_line.return_value = "0,0,50.000"
        z = self.test_prober.siph.get_nanocube_z(ProbePosition.West)
        self.mock_comm.send.assert_called_with("siph:get_nanocube_z West")
        self.assertEqual(z, 50.000)

    def test_start_tracking(self):
        """Test start_tracking method."""
        self.mock_comm.read_line.return_value = "0,5,OK"
        command_id = self.test_prober.siph.start_tracking(30)
        self.mock_comm.send.assert_called_with("siph:start_tracking 30")
        self.assertEqual(command_id, 5)


if __name__ == "__main__":
    unittest.main()
