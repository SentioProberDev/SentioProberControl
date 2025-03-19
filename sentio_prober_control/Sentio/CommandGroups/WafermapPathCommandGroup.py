from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import RoutingPriority, RoutingStartPoint, TestSelection
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class WafermapPathCommandGroup(CommandGroupBase):
    """This command group bundles functions for setting up and using the test path of the wafermap.

    A test path defines which dies are tested in which order.
    """

    def create_from_bin(self, bin_val: int) -> None:
        """Create test path by using all dies with a specific bin.

        Wraps SENTIO's map:path:create_from_bin remote command.

        Args:
            bin_val: The bin value to use.
        """
        self.comm.send("map:path:create_from_bins {0}".format(bin_val))
        Response.check_resp(self.comm.read_line())


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
        self.comm.send(f"map:path:select_dies {selection.toSentioAbbr()}")
        Response.check_resp(self.comm.read_line())


    def set_routing(self, sp: RoutingStartPoint, pri: RoutingPriority) -> None:
        """Set up path finnding for stepping by specifying a start point position
        and a row or column priority for routing.

        Wraps SENTIO's map:set_routing remote command.

        Args:
            sp: The start point of the routing.
            pri: The priority of the routing (rows first, columns first).
        """
        self.comm.send(f"map:set_routing {sp.toSentioAbbr()}, {pri.toSentioAbbr()}")
        Response.check_resp(self.comm.read_line())
