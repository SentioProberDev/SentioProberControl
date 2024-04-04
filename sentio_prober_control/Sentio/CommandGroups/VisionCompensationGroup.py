from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import CompensationMode, CompensationType
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase

from deprecated import deprecated


class VisionCompensationGroup(CommandGroupBase):
    """This command group contains functions for working with x,y and z compensation.

    You are not meant to instantiate this class directly. Access it via the compensation attribute
    of the vision attribute of the [SentioProber](SentioProber.md) class.
    """

    def __init__(self, comm):
        super().__init__(comm)


    @deprecated("Use vision.compensation.enable() instead")
    def set_compensation(self, comp: CompensationMode, enable: bool) -> Tuple[str, str]:
        self.comm.send(f"vis:compensation:enable {comp.toSentioAbbr()}, {enable}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], tok[1]


    def enable(self, comp: CompensationMode, enable: bool) -> Tuple[str, str]:
        """Enable or disable compensation for a given subsystem.

        Wraps Sentios "vis:compensation:enable" command.

        Args:
            comp: The compensation to enable or disable.
            enable: True to enable, False to disable.

        Returns:
            XY-Mode: State of the XY compensation.
            Z-Mode: State of the Z compensation.
        """

        self.comm.send(f"vis:compensation:enable {comp.toSentioAbbr()}, {enable}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], tok[1]


    def start_execute(self, type: CompensationType, mode: CompensationMode) -> Response:
        """Start the execution of a compensation.

        Wraps Sentios "vis:compensation:start_execute" remote command.

        Args:
            type: The type of compensation to execute.
            mode: The mode of compensation to execute.

        Returns:
            A Response object.
        """

        self.comm.send(f"vis:compensation:start_execute {type.toSentioAbbr()}, {mode.toSentioAbbr()}")
        return Response.check_resp(self.comm.read_line())
