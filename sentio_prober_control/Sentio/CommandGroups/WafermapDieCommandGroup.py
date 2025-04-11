from typing import Tuple
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class WafermapDieCommandGroup(CommandGroupBase):
    """This Command group bundles commands for setting up dies on a wafermap."""

    def add(self, x: int, y: int) -> None:
        """Add a die to the wafermap. If the die is already part of the map, nothing happens.

        Args:
            x: The column of the die.
            y: The row of the die.
        """
        self.comm.send(f"map:die:add {x}, {y}")
        Response.check_resp(self.comm.read_line())

    def remove(self, x: int, y: int) -> None:
        """Remove a die from the wafermap.

        This will mark the die as nonexistent and make it unavailable for stepping.
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
        self.comm.send(f"map:die:select {x}, {y}")
        Response.check_resp(self.comm.read_line())

    def unselect(self, x: int, y: int) -> None:
        """Unselects a die from testing by removing it from the test path.

        Args:
            x: The column of the die.
            y: The row of the die.
        """
        self.comm.send(f"map:die:unselect {x}, {y}")
        Response.check_resp(self.comm.read_line())

    def get_current_index(self) -> Tuple[int, int, int]:
        """Retrieves information about the current die.

        Returns:
            A tuple containing:
                - List Index (int): The index in the routing list.
                - Column Index (int): The column index relative to the grid origin.
                - Row Index (int): The row index relative to the grid origin.
        """
        self.comm.send("map:die:get_current_index")
        resp = Response.check_resp(self.comm.read_line())

        values = resp.message().split(",")
        if len(values) < 3:
            raise ValueError(f"Invalid response: {resp.message()}")

        return int(values[0]), int(values[1]), int(values[2])

    def get_status(self, col_index: int, row_index: int) -> int:
        """Retrieves information about presence and selection of a die.

        Args:
            col_index: Column of the die relative to the grid origin.
            row_index: Row number of the die relative to the grid origin.

        Returns:
            Status (int):
                - `1`: Die is selected.
                - `2`: Die is not selected.
                - `3`: Die is not present.
        """
        self.comm.send(f"map:die:get_status {col_index}, {row_index}")
        resp = Response.check_resp(self.comm.read_line())

        return int(resp.message())

    def get_current_subsite(self) -> int:
        """Retrieves information about the currently active subsite.

        Returns:
            Subsite Index (int): The index of the currently active subsite.
        """
        self.comm.send("map:die:get_current_subsite")
        resp = Response.check_resp(self.comm.read_line())

        return int(resp.message())
