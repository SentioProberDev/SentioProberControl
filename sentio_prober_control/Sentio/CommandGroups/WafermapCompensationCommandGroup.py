from deprecated import deprecated
from sentio_prober_control.Sentio.Enumerations import ExecuteAction, XyCompensationType, ZCompensationType
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


@deprecated("Use VisionCompensationGroup instead")
class WafermapCompensationCommandGroup(CommandGroupBase):
    """This command group bundles functions for setting up and using XY/Z compensation on the wafermap."""

    @deprecated("Use vision.compensation.enable instead")
    def topography(self, execute: ExecuteAction) -> Response:
        """Execute topography compensation.

        Args:
            execute: The action to execute.

        Returns:
            The command ID of the asynchronous operation.
        """
        self.comm.send(f"map:compensation:topography {execute.to_string()}")
        resp = Response.check_resp(self.comm.read_line())

        if not resp.ok():
            raise ProberException(resp.message())

        return resp

    def set_xy(self, comp_type: XyCompensationType) -> None:
        """Enable the XY Stepping Compensation.

        Args:
            comp_type: The type of XY Stepping Compensation.
        """
        self.comm.send(f"map:compensation:set_xy {comp_type.to_string()}")
        Response.check_resp(self.comm.read_line())

    def set_z(self, comp_type: ZCompensationType) -> None:
        """Enable the Z Stepping Compensation.

        Args:
            comp_type: The type of Z Stepping Compensation.
        """
        self.comm.send(f"map:compensation:set_z {comp_type.to_string()}")
        Response.check_resp(self.comm.read_line())
