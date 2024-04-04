from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class WafermapDieCommandGroup(CommandGroupBase):
    """This Command group bundles commands for setting up dies on a wafermap."""

    def add(self, x: int, y: int) -> None:
        """Add a die to the wafermap. If the die is already part of the map
        nothing happens.

        Args:
            x: The column of the die.
            y: The row of the die.
        """
        self.comm.send(f"map:die:add {x}, {y}")
        Response.check_resp(self.comm.read_line())


    def remove(self, x: int, y: int) -> None:
        """Remove a die from the wafermap.

        This will mark the die as nonexistant and make it unavailable for stepping.
        Removed dies are treated as if they were physically not present on the wafer.

        Wraps SENTIO's map:die:remove remote command.

        Args:
            x: The column of the die.
            y: The row of the die.
        """
        self.comm.send(f"map:die:remove {x}, {y}")
        Response.check_resp(self.comm.read_line())


    def select(self, x: int, y: int) -> None:
        """Selects a die for testing by adding it to the test path.

        Args:
            x: The column of the die.
            y: The row of the die.
        """
        self.comm.send(f"map:die:add {x}, {y}")
        Response.check_resp(self.comm.read_line())


    def unselect(self, x: int, y: int) -> None:
        """Unselects a die from testing by removing it from the test path.

        Args:
            x: The column of the die.
            y: The row of the die.
        """
        self.comm.send(f"map:die:unselect {x}, {y}")
        Response.check_resp(self.comm.read_line())
