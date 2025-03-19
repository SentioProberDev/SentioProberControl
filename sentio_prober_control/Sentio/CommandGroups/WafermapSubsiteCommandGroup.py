from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import AxisOrient, StatusBits
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class WafermapSubsiteGroup(CommandGroupBase):
    """Represents the wafermap subsite command group which provides
    functionality for setting up und stepping over subsites.
    """

    def __init__(self, comm, wafermap_command_group) -> None:
        """Creates a new WafermapSubsiteGroup object.

        You are not meant to directly create objects of this class.
        """
        super().__init__(comm)
        self._parent_command_group = wafermap_command_group


    def add(self, id: str, x: float, y: float, orient: AxisOrient = AxisOrient.UpRight) -> None:
        """Add a single subsite to the wafermap.

        Creates a new subsite definition in SENTIO. The subsite position is defined
        relative to the die home position. This is the chuck home position projected onto
        the current die.

        Wraps the "map:subsite:add" remote command.

        Args:
            id: The subsite id.
            x: The x position of the subsite in micrometer as an offset to the die home position.
            y: The y position of the subsite in micrometer as an offset to the die home position.
            orient: The axis orientation used fot the submitted values
        """
        self.comm.send("map:subsite:add {}, {}, {}, {}".format(id, x, y, orient.toSentioAbbr()))
        Response.check_resp(self.comm.read_line())


    def bin_step_next(self, bin: int) -> Tuple[int, int, int]:
        """Step to the next active subsite and assign bin code to current subsite.

        Wraps the "map:subsite:bin_step_next" remote command.

        Args:
            bin: The bin code to assign to the current subsite.

        Returns:
            A tuple containing the wafermap row, column and subsite index after the step.
        """
        self.comm.send(f"map:subsite:bin_step_next {bin}")

        resp = Response.check_resp(self.comm.read_line())
        self._parent_command_group.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute

        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])


    def get(self, idx: int, orient: AxisOrient | None = None) -> Tuple[str, float, float]:
        """Returns the subsite definition for a subsite with a given index.

        Wraps the "map:subsite:get" remote command.

        Args:
            idx: The index of the subsite.
            orient: The axis orientation used for the returned subsite coordinates. If this parameter is omitted the axis orientation of the wafer map is used.

        Returns:
            A tuple containing the subsite id, the x position and the y position of the subsite.
            X and y positions are relative to the die home position.
        """

        # If no orientation is given use the map axis orientation. The SENTIO remote command would always default to UpRight which may 
        # not be correct if the map has a different orientation.
        if orient is None:
            orient_str = "MAP"
        else:
            orient_str = orient.toSentioAbbr()

        self.comm.send(f"map:subsite:get {idx}, {orient_str}")
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return str(tok[0]), float(tok[1]), float(tok[2])


    def get_num(self) -> int:
        """Retrieve the number of subsites per die defined in the wafermap.

        Wraps the "map:subsite:get_num" remote command.

        Returns:
            The number of subsites in the wafermap.
        """
        self.comm.send("map:subsite:get_num")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())


    def reset(self) -> None:
        """Reset Sentios subsite definitions.

        Wraps the "map:subsite:reset" remote command.
        """
        self.comm.send("map:subsite:reset")
        Response.check_resp(self.comm.read_line())


    def step_next(self) -> Tuple[int, int, int]:
        """Step to the next active subsite.

        Wraps the "map:subsite:step_next" remote command.

        Returns:
            A tuple containing the wafermap row, column and subsite index after the step.
        """
        self.comm.send("map:subsite:step_next")

        resp = Response.check_resp(self.comm.read_line())
        self._parent_command_group.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute

        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])
