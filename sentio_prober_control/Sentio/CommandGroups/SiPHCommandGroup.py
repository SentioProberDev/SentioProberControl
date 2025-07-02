from typing import Tuple

from sentio_prober_control.Sentio.Compatibility import Compatibility, CompatibilityLevel
from sentio_prober_control.Sentio.Enumerations import ProbePosition, UvwAxis, FiberType, CompatibilityLevel, Stage
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class SiPHCommandGroup(CommandGroupBase):
    """This command group contains functions for working with SiPH applications.
    You are not meant to instantiate this class directly. Access it via the siph attribute
    of the [SentioProber](SentioProber.md) class.
    """

    def __init__(self, prober : 'SentioProber') -> None:
        super().__init__(prober)


    def fast_alignment(self) -> None:
        """Perform fast fiber alignment."""
        self.comm.send("siph:fast_alignment")
        Response.check_resp(self.comm.read_line())


    def get_cap_sensor(self) -> Tuple[float, float]:
        """Get the capacitance sensor value.

        Returns:
            A tuple with the values from the capacity sensors of probe 1 and probe 2.
        """
        self.comm.send("siph:get_cap_sensor")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def get_fiber_length(self, stage: Stage, probe: ProbePosition) -> float:
        """Retrieves the fiber length of an SiPH positioner.

        Args:
            stage: The probe stage (TopProbe/BottomProbe).
            probe: The probe position.

        Returns:
            The fiber length in micrometer.
        """
        if stage == Stage.TopProbe:
            pos = 'top'
        elif stage == Stage.BottomProbe:
            pos = 'bottom'
        else:
            raise ValueError("Stage must be a probe stage")

        self.comm.send(f"siph:{pos}:{probe.to_string().lower()}:get_fiber_length")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_intensity(self, channel : int = 1) -> float:
        """Get the current intensity value.

         Args:
            channel: The channel to return the intensite of. One-Based index, must be either 1 or 2.
        """

        self.comm.send(f"siph:get_intensity {channel}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def gradient_search(self) -> None:
        """Execute SiPh gradient search.

           Returns:
                None
        """

        self.comm.send("siph:gradient_search")
        Response.check_resp(self.comm.read_line())


    def move_hover(self, probe: ProbePosition) -> None:
        """Move SiPh probe to hover height.

        Args:
            probe: The probe on which the SiPh probe is mounted.
        """

        self.comm.send(f"siph:move_hover {probe.to_string()}")
        Response.check_resp(self.comm.read_line())


    def move_separation(self, probe: ProbePosition) -> None:
        """Move SiPh probe to separation height.

        Args:
            probe: The probe on which the SiPh probe is mounted.

        Returns:
            None
        """

        self.comm.send(f"siph:move_separation {probe.to_string()}")
        Response.check_resp(self.comm.read_line())


    def coupling(self, probe: ProbePosition, axis: UvwAxis) -> None:
        """Start execute coupling.

        Args:
            probe: Execute probe.
            axis: Execute axis
        """

        self.comm.send(f"siph:coupling {probe.to_string()},{axis.to_string()}")
        Response.check_resp(self.comm.read_line())


    def get_alignment(self, probe: ProbePosition, fiber_type: FiberType) -> Tuple[bool, bool, bool, bool]:
        """Get the fast alignment function enable including Coarse, Fine, Gradient, and Rotary/Focal searching.

        Args:
            probe: The probe to get the alignment settings for.
            fiber_type: The type of fiber used (Single, Array, or Lensed).

        Returns:
            A tuple containing the status of Coarse, Fine, Gradient, and Rotary/Focal searching (True/False).
        """
        self.comm.send(f"siph:get_alignment {probe.to_string()},{fiber_type.to_string()}")
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        coarse = tok[0].strip().lower() == "true"
        fine = tok[1].strip().lower() == "true"
        gradient = tok[2].strip().lower() == "true"
        rotary_focal = tok[3].strip().lower() == "true"

        return coarse, fine, gradient, rotary_focal


    def set_origin(self, probe: ProbePosition) -> None:
        """Set the current position as the origin position for the SiPH positioner.

        Args:
            probe: The probe to set the origin position for (East or West).

        Returns:
            A Response object containing the command execution status.
        """

        self.comm.send(f"siph:set_origin {probe.to_string()}")
        Response.check_resp(self.comm.read_line())


    def move_origin(self, probe: ProbePosition) -> None:
        """Move SiPH positioner to its origin position.

        The movement includes:
        - NanoCube XY moves back to 50 μm.
        - UVW axes move back to the position set during Hover Height training.
        - If the axis is in "Manual" mode, only NanoCube moves to 50 μm.

        Args:
            probe: The probe to move to origin position (East or West).

        Returns:
            A Response object containing the command execution status.
        """
        self.comm.send(f"siph:move_origin {probe.to_string()}")
        Response.check_resp(self.comm.read_line())


    def move_position_uvw(self, probe: ProbePosition, axis: UvwAxis, degree: float) -> float:
        """Move the SiPH positioner target axis with a relative degree.

        Args:
            probe: The positioner ID to move (East or West).
            axis: The axis to move (U, V, or W).
            degree: The relative degree to move.

        Returns:
            The current position of the axis after movement.
        """
        self.comm.send(f"siph:move_position_uvw {probe.to_string()},{axis.to_string()},{degree}")
        resp = Response.check_resp(self.comm.read_line())

        return float(resp.message())


    def pivot_point(self, probe: ProbePosition) -> None:
        """Run pivot point calibration for the specified positioner.

        Args:
            probe: The positioner ID to calibrate (East or West).

        Returns:
            A Response object containing the command execution status.
        """
        self.comm.send(f"siph:pivot_point {probe.to_string()}")
        Response.check_resp(self.comm.read_line())


    def set_alignment(self, probe: ProbePosition, fiber_type: FiberType, coarse: bool, fine: bool, gradient: bool,
                      rotary: bool) -> None:
        """Set the fast alignment function enable including Coarse, Fine, Gradient, and Rotary/Focal searching.

        Args:
            probe: The positioner ID to calibrate (East or West).
            fiber_type: The fiber type ("Single", "Array", "Lensed").
            coarse: Enable or disable coarse search (True = ON, False = OFF).
            fine: Enable or disable fine search (True = ON, False = OFF).
            gradient: Enable or disable gradient search (True = ON, False = OFF).
            rotary: Enable or disable rotary/focal search (True = ON, False = OFF, not supported for "Single" fiber type).

        Returns:
            A Response object containing the command execution status.
        """
        coarse_str = "ON" if coarse else "OFF"
        fine_str = "ON" if fine else "OFF"
        gradient_str = "ON" if gradient else "OFF"
        rotary_str = "ON" if rotary else "OFF"

        self.comm.send(f"siph:set_alignment {probe.to_string()},{fiber_type},{coarse_str},{fine_str},{gradient_str},{rotary_str}")
        Response.check_resp(self.comm.read_line())

    def set_hover(self, stage: Stage, probe: ProbePosition, gap: float) -> None:
        """Sets the hover gap of an SiPH positioner.

        Args:
            stage: The probe stage (TopProbe/BottomProbe).
            probe: The probe position.

        Returns:
            A Response object containing the command execution status.
        """
        if stage == Stage.TopProbe:
            pos = 'top'
        elif stage == Stage.BottomProbe:
            pos = 'bottom'
        else:
            raise ValueError("Stage must be a probe stage")

        self.comm.send(f"siph:{pos}:{probe.to_string().lower()}:set_hover {gap}")
        Response.check_resp(self.comm.read_line())


    def set_pivot_point(self, rotary_angle_1: float, rotary_angle_2: float, leveling_angle: float, repeats: int) -> None:
        """Set the parameters for the pivot point function.

        Args:
            rotary_angle_1: The first rotary angle.
            rotary_angle_2: The second rotary angle.
            leveling_angle: The leveling angle.
            repeats: The number of repetitions.

        Returns:
            A Response object containing the command execution status.
        """
        self.comm.send(f"siph:set_pivot_point {rotary_angle_1},{rotary_angle_2},{leveling_angle},{repeats}")
        Response.check_resp(self.comm.read_line())


    def download_graph_data(self, file_path: str, file_name: str) -> None:
        """Download the graph data and save it to the specified location.

        Args:
            file_path: The directory path where the graph data will be saved.
            file_name: The name of the file to save the graph data.

        Returns:
            A Response object containing the command execution status.
        """
        Compatibility.assert_min(CompatibilityLevel.Sentio_25_2)

        self.comm.send(f"siph:download_graph_data {file_path}, {file_name}")
        Response.check_resp(self.comm.read_line())


    def start_tracking(self, timeout: int = 60) -> int:
        """Start the SiPH positioner gradient tracking search asynchronously.

        Args:
            timeout: Timeout value in seconds (range: 1~600). Default is 60 sec.

        Returns:
            The asynchronous command ID, which can be used to check status or abort.
        """
        self.comm.send(f"siph:start_tracking {timeout}")
        resp = Response.check_resp(self.comm.read_line())

        # Extract asynchronous command ID from response
        command_id = int(resp.cmd_id())
        return command_id


    def move_nanocube_xy(self, probe: ProbePosition, x: float, y: float) -> tuple[float, float]:
        """Move NanoCube to the target XY position.

        The movement range is limited to 0 ~ 100 μm.

        Args:
            probe: The positioner (East or West).
            x: Target X position (μm), must be in range [0, 100].
            y: Target Y position (μm), must be in range [0, 100].

        Returns:
            A tuple containing the new X and Y positions after movement.
        """
        if not (0 <= x <= 100 and 0 <= y <= 100):
            raise ValueError("X and Y values must be between 0 and 100 μm.")

        self.comm.send(f"move_nanocube_xy {probe.to_string()},{x},{y}")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        new_x = float(tok[0])
        new_y = float(tok[1])
        return new_x, new_y


    def get_nanocube_xy(self, probe: ProbePosition) -> tuple[float, float]:
        """Get the current NanoCube XY position.

        Args:
            probe: The positioner (East or West).

        Returns:
            A tuple containing the current X and Y positions.
        """
        self.comm.send(f"get_nanocube_xy {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        current_x = float(tok[0])
        current_y = float(tok[1])
        return current_x, current_y


    def get_nanocube_z(self, probe: ProbePosition) -> float:
        """Get the current NanoCube Z position.

        Args:
            probe: The positioner (East or West).

        Returns:
            The current Z position.
        """
        self.comm.send(f"get_nanocube_z {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        current_z = float(tok[0])
        return current_z