from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import ( FindPatternReference, CameraMountPoint, DefaultPattern )
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class VisionPatternCommandGroup(CommandGroupBase):
    """This command group bundles functions for setting up and using the pattern."""

    def find(self, name: str, threshold: float = 70, pattern_index: int = 0, reference: FindPatternReference = FindPatternReference.CenterOfRoi) -> Tuple[float, float, float, float]:
        """Find a trained pattern in the camera image.

        Args:
            name: The name of the pattern to find.
            threshold: The detection threshold. The higher the threshold, the more certain the detection must be.
            pattern_index: The index of the pattern to find. In SENTIO each pattern may have up to 5 alternate patterns. This is the index of the alternate pattern.
            reference: The reference point to use for the pattern detection.
        """

        self.comm.send(f"vis:find_pattern {name}, {threshold}, {pattern_index}, {reference.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2]), float(tok[3])

    def get_chuck_pos(self, camera: CameraMountPoint, pattern: DefaultPattern) -> Tuple[float, float]:
        """Get the chuck XY position associated with a trained pattern.

        Args:
            camera: The camera mount point (e.g., Scope).
            pattern: The name of the trained pattern.

        Returns:
            A tuple with the X and Y coordinates in micrometers.
        """
        self.comm.send(f"vis:pattern:get_chuck_pos {camera.to_string()}, {pattern.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def set_chuck_pos(self, camera: CameraMountPoint, pattern: DefaultPattern, x: float, y: float) -> Tuple[float, float]:
        """Set the chuck XY position associated with a trained pattern.

        Args:
            camera: The camera mount point (e.g., Scope).
            pattern: The name of the pattern.
            x: The X coordinate to assign in micrometers.
            y: The Y coordinate to assign in micrometers.

        Returns:
            A tuple with the confirmed X and Y coordinates.
        """
        self.comm.send(f"vis:pattern:set_chuck_pos {camera.to_string()}, {pattern.to_string()}, {x}, {y}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def show_training_box(self, visible: bool = True) -> None:
        """Show or hide the pattern training box on the vision UI.

        Args:
            visible: True to show the box, False to hide it.
        """
        self.comm.send(f"vis:pattern:show_training_box {str(visible).lower()}")
        Response.check_resp(self.comm.read_line())

    def train(self, pattern: str) -> None:
        """Train a new pattern using the current training box.

        Args:
            pattern: The name of the pattern to store.
        """
        self.comm.send(f"vis:pattern:train {pattern}")
        Response.check_resp(self.comm.read_line())