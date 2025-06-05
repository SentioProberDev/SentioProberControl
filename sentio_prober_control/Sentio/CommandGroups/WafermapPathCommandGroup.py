from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import RoutingPriority, RoutingStartPoint, TestSelection, PathSelection
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class WafermapPathCommandGroup(CommandGroupBase):
    """This command group bundles functions for setting up and using the test path of the wafermap.

    A test path defines which dies are tested in which order.
    """

    def create_from_bin(self, bin_val: int | str | PathSelection) -> int:
        """Create test path by using all dies with a specific bin.

        Wraps SENTIO's map:path:create_from_bin remote command.

        Args:
            bin_val: The bin value to use. Can be an int or PathSelection enum.
        """
        if isinstance(bin_val, PathSelection):
            bin_val_str = bin_val.to_string()
        else:
            bin_val_str = str(bin_val)

        self.comm.send(f"map:path:create_from_bins {bin_val_str}")
        resp = Response.check_resp(self.comm.read_line())

        return int(resp.message())

    def get_die(self, seq: int) -> Tuple[int, int]:
        """Get die column and row coordinates from a sequence number.

        Wraps SENTIO's map:path:get_die remote command.

        Args:
            seq: The sequence number of the die.

        Returns:
            A tuple with the column and row coordinates of the die.
        """
        self.comm.send("map:path:get_die {0}".format(seq))
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1])

    def select_dies(self, selection: TestSelection) -> None:
        """Select dies for testing.

        Wraps SENTIO's map:path:select_dies remote command.

        Args:
            selection: The selection of dies to select.
        """
        self.comm.send(f"map:path:select_dies {selection.to_string()}")
        Response.check_resp(self.comm.read_line())

    def set_routing(self, sp: RoutingStartPoint, pri: RoutingPriority) -> None:
        """Set up path finnding for stepping by specifying a start point position
        and a row or column priority for routing.

        Wraps SENTIO's map:set_routing remote command.

        Args:
            sp: The start point of the routing.
            pri: The priority of the routing (rows first, columns first).
        """
        self.comm.send(f"map:set_routing {sp.to_string()}, {pri.to_string()}")
        Response.check_resp(self.comm.read_line())

    def add_bins(self, selection: int | list[int] | range | list[range]) -> int:
        """
        Adds dies with specific bin values to the stepping path.

        This method simplifies usage by accepting native Python types instead of custom strings,
        making it easier to dynamically construct input data.

        Args:
            selection (int | list[int] | range | list[range]):
                - A single bin number (e.g. 1)
                - A list of bin numbers (e.g. [1, 3, 5])
                - A range object (e.g. range(1, 6)) → "1-5"
                - A list of ranges or mix of int/range (e.g. [range(1, 4), 10])

        Returns:
            int: The resulting path length after adding the dies.

        Raises:
            TypeError: If the input contains unsupported data types.
        """
        if isinstance(selection, int):
            # Single bin value
            selection_str = str(selection)

        elif isinstance(selection, range):
            # Convert range to SENTIO format: "start-end"
            selection_str = f"{selection.start}-{selection.stop - 1}"

        elif isinstance(selection, list):
            parts = []
            for item in selection:
                if isinstance(item, range):
                    parts.append(f"{item.start}-{item.stop - 1}")
                elif isinstance(item, int):
                    parts.append(str(item))
                else:
                    raise TypeError(f"Unsupported item type in list: {type(item)}")
            selection_str = ",".join(parts)

        else:
            raise TypeError(f"Unsupported selection type: {type(selection)}")

        self.comm.send(f"map:path:add_bins {selection_str}")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())

    def remove_bins(self, selection: int | list[int] | range | list[range]) -> int:
        """
        Removes dies with specific bin values from the stepping path.

        This method allows more natural Python inputs, avoiding manual string construction.

        Args:
            selection (int | list[int] | range | list[range]):
                - A single bin number (e.g. 2)
                - A list of bin numbers (e.g. [1, 4, 6])
                - A range (e.g. range(5, 10)) → becomes "5-9"
                - A list of ranges or combination (e.g. [range(1, 4), 6])

        Returns:
            int: Remaining path length after removal.

        Raises:
            TypeError: If the selection type is not supported.
        """
        if isinstance(selection, int):
            selection_str = str(selection)

        elif isinstance(selection, range):
            selection_str = f"{selection.start}-{selection.stop - 1}"

        elif isinstance(selection, list):
            parts = []
            for item in selection:
                if isinstance(item, range):
                    parts.append(f"{item.start}-{item.stop - 1}")
                elif isinstance(item, int):
                    parts.append(str(item))
                else:
                    raise TypeError(f"Unsupported item in list: {type(item)}")
            selection_str = ",".join(parts)

        else:
            raise TypeError(f"Unsupported selection type: {type(selection)}")

        self.comm.send(f"map:path:remove_bins {selection_str}")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())

