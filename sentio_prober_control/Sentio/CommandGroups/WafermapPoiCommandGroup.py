from sentio_prober_control.Sentio.Enumerations import PoiReferenceXy, Stage
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class WafermapPoiCommandGroup(CommandGroupBase):
    """A command group for working with Points of Interest (POI) on the wafermap."""

    def add(self, x: float, y: float, desc: str) -> None:
        """Add a POI to the list.

        Wraps SENTIO's map:poi:add remote command.

        Args:
            x: The x coordinate of the POI.
            y: The y coordinate of the POI.
            desc: The description of the POI.
        """
        self.comm.send(f"map:poi:add {x}, {y}, {desc}")
        Response.check_resp(self.comm.read_line())

    def get(self, idx: int) -> tuple[float, float, str]:
        """Get POI data of a single POI.

        Wraps SENTIO's map:poi:get remote command.

        Args:
            idx: The index of the POI to retrieve.

        Returns:
            A tuple (x, y, description) of the POI.
        """
        self.comm.send(f"map:poi:get {idx}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), str(tok[2])

    def get_num(self) -> int:
        """Returns the number of POIs in the list.

        Wraps SENTIO's map:poi:get_num remote command.

        Returns:
            The number of POIs in the list.
        """
        self.comm.send("map:poi:get_num")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())

    def reset(self, stage: Stage, refXy: PoiReferenceXy) -> None:
        """Reset the list of POIs.

        Clears the list and resets its stage and position reference settings.

        Wraps SENTIO's map:poi:reset remote command.

        Args:
            stage: The stage to reset the POIs for.
            refXy: The reference point for the POIs.
        """
        self.comm.send("map:poi:reset {0}, {1}".format(stage.to_string(), refXy.to_string()))
        Response.check_resp(self.comm.read_line())

    def step(self, target: str | int) -> tuple[int, int, int]:
        """Step to a POI in the list.

        Wraps SENTIO's map:poi:step remote command.

        Args:
            target: The target POI to step to. This is either the index of the poi or the id of the poi.
        """
        self.comm.send(f"map:poi:step {target}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])

    def step_first(self) -> tuple[int, int, int]:
        """Step to the first POI in the list.

        Wraps SENTIO's map:poi:step_first remote command.
        """
        self.comm.send("map:poi:step_first")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])

    def step_next(self) -> tuple[int, int, int]:
        """Step to the next POI in the list.

        Wrap SENTIO's map:poi:step_next remote command.
        """
        self.comm.send("map:poi:step_next")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])

    def remove(self, idx: int | None = None) -> None:
        """Remove POI(s) from wafermap.

        Wraps SENTIO's map:poi:remove remote command.

        Args:
            idx: POI index to remove. If None, remove all.
        """
        if idx is None:
            self.comm.send("map:poi:remove")
        else:
            self.comm.send(f"map:poi:remove {idx}")
        Response.check_resp(self.comm.read_line())
