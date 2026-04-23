from sentio_prober_control.Sentio.Enumerations import CompensationMode, CompensationType
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase

from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from sentio_prober_control.Sentio.ProberSentio import SentioProber

class VisionCompensationGroup(CommandGroupBase):
    """This command group contains functions for working with x,y and z compensation.

    You are not meant to instantiate this class directly. Access it via the compensation attribute
    of the vision attribute of the [SentioProber](SentioProber.md) class.
    """

    def __init__(self, prober : SentioProber) -> None:
        super().__init__(prober)


    def set_compensation(self, comp: CompensationMode, enable: bool) -> Tuple[str, str]:
        """Enable or disable compensation.
        
            !!! danger "Deprecated since Sentio 25.2<br/>\
            This function is obsolete and will be removed in a future release.\
            Use vision.compensation.enable instead"
        """
        return self.enable(comp, enable)


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

        self.comm.send(f"vis:compensation:enable {comp.to_string()}, {enable}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        if len(tok) < 2:
            raise ValueError(f"Expected 2 values in response message, got {len(tok)}: '{resp.message()}'")
        
        return tok[0], tok[1]

    def start_execute(self, compensation_type: CompensationType, mode: CompensationMode | None = None, moveToOffset: bool | None = None) -> Response:
        """Start the execution of a compensation.

        Wraps Sentios "vis:compensation:start_execute" remote command.

        This function was rewritten to fix #49 (https://github.com/SentioProberDev/SentioProberControl/issues/49). 
        The two last parameters are optional, moveToOffset parameter was added.

        Args:
            compensation_type: The type of compensation to execute.
            mode: The mode of compensation to execute.
            moveToOffset: Move to the offset position. Only applicable with type=CompensationType.DieAlign and mode!=CompensationMode.ProbeCard.

        Returns:
            A Response object.
        """

        if moveToOffset is not None and mode is None:
            raise ValueError("moveToOffset cannot be used without a mode.")
        
        if mode is not None and moveToOffset is not None:
            self.comm.send(f"vis:compensation:start_execute {compensation_type.to_string()}, {mode.to_string()}, {moveToOffset}")  
        elif mode is not None:
            self.comm.send(f"vis:compensation:start_execute {compensation_type.to_string()}, {mode.to_string()}")
        else:
            self.comm.send(f"vis:compensation:start_execute {compensation_type.to_string()}")

        return Response.check_resp(self.comm.read_line())
