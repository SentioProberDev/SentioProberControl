from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class WafermapViewCommandGroup(CommandGroupBase):
    """This command group provides functions related to wafermap view settings."""

    def show_current_die(self) -> None:
        """Show the current die in the wafermap view.

        Wraps SENTIO's "map:view:show_current_die" remote command.
        """
        self.comm.send("map:view:show_current_die")
        Response.check_resp(self.comm.read_line())
