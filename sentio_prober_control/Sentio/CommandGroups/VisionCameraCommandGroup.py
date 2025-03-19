from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import AutoFocusAlgorithm, CameraMountPoint, DefaultPattern
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class VisionCameraCommandGroup(CommandGroupBase):
    """A command group for setting camera parameters.

    You are not meant to instantiate this class directly. Access it via the camera attribute
    of the vision attribute of the [SentioProber](SentioProber.md) class.
    """

    def __init__(self, comm) -> None:
        super().__init__(comm)


    def set_light(self, mp: CameraMountPoint, value: int) -> Response:
        """Set intensity of the light.

        Args:
            mp: The mount point of the camera.
            value: The intensity of the light.
        """

        self.comm.send(f"vis:set_prop light, {mp.toSentioAbbr()}, {value}")
        return Response.check_resp(self.comm.read_line())


    def set_exposure(self, mp: CameraMountPoint, value: int) -> Response:
        """Set exposure time of the camera.

        Args:
            mp: The mount point of the camera.
            value: The exposure time in microseconds.

        Returns:
            A Response object.
        """

        self.comm.send(f"vis:set_prop exposure, {mp.toSentioAbbr()}, {value}")
        return Response.check_resp(self.comm.read_line())


    def set_gain(self, mp: CameraMountPoint, value: float) -> Response:
        """Set gain of the camera.

        Args:
            mp: The mount point of the camera.
            value: The gain value.
        """

        self.comm.send(f"vis:set_prop gain, {mp.toSentioAbbr()}, {value}")
        return Response.check_resp(self.comm.read_line())


    def get_light(self, mp: CameraMountPoint) -> float:
        """Get light intensity.

        Args:
            mp: The mount point of the camera.
        """

        self.comm.send(f"vis:get_prop light, {mp.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_exposure(self, mp: CameraMountPoint) -> float:
        """Get exposure time.

        Args:
            mp: The mount point of the camera.

        Returns:
            The exposure time in microseconds.
        """

        self.comm.send(f"vis:get_prop exposure, {mp.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_focus_value(self, mp: CameraMountPoint, alg: AutoFocusAlgorithm) -> float:
        """Get the focus value of the camera.

        This function wraps the vis:get_focus_value remote command.

        Args:
            mp: The mount point of the camera.
            alg: The autofocus algorithm to use.

        Returns:
            The focus value.
        """

        self.comm.send(
            f"vis:get_focus_value {mp.toSentioAbbr()}, {alg.toSentioAbbr()}"
        )
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_gain(self, mp: CameraMountPoint) -> float:
        """Get gain of the camera.

        Args:
            mp: The mount point of the camera.

        Returns:
            The gain value.
        """

        self.comm.send(f"vis:get_prop gain, {mp.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_calib(self, mp: CameraMountPoint) -> Tuple[float, float]:
        """Get the calibration data of the camera.

        Camera calibration data consists of the width and height of
        an image pixel in micrometers.

        Args:
            mp: The mount point of the camera.

        Returns:
            width: Get the width of a camera pixel in micrometers.
            height: Get height of a camera pixel in micrometers.
        """

        self.comm.send(f"vis:get_prop calib, {mp.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_image_size(self, mp: CameraMountPoint) -> Tuple[int, int]:
        """Get size of the image.

        Args:
            mp: The mount point of the camera.

        Returns:
            width: The width of the image in pixels.
            height: The height of the image in pixels.
        """

        self.comm.send(f"vis:get_prop image_size, {mp.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1])


    def is_pattern_trained(self, mp: CameraMountPoint, pat) -> bool:
        """Check if a pattern is trained.

        This command wraps the vis:pattern:is_trained remote command.

        Args:
            mp: The mount point of the camera.

        Returns:
            True if the pattern is trained, False otherwise.
        """

        if isinstance(pat, DefaultPattern):
            pattern_name = pat.toSentioAbbr()
        else:
            pattern_name = pat

        self.comm.send(f"vis:pattern:is_trained {mp.toSentioAbbr()}, {pattern_name}")
        resp = Response.check_resp(self.comm.read_line())
        is_trained = resp.message() == "1"
        return is_trained
