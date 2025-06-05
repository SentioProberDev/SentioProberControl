from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import XyReference, Stage
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class ScopeCommandGroup(CommandGroupBase):
    """This command group contains functions for working with motorized scopes.
    You are not meant to instantiate this class directly. Access it via the probe attribute
    of the [SentioProber](SentioProber.md) class.

    Example:

    ```py
    from sentio_prober_control.Sentio.ProberSentio import SentioProber

    prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
    prober.scope.move_probe_xy(XyReference.Current, 1000, 2000)
    ```
    """

    def __init__(self, prober: 'SentioProber', stage : Stage, has_subgroups = False) -> None:
        super().__init__(prober)

        if stage==Stage.Scope:
            self.__scope_selector: str = "top"
        elif stage==Stage.BottomScope:
            self.__scope_selector: str = "bottom"
        elif stage==Stage.AuxiliaryScope:
            self.__scope_selector: str = "aux"
        else:
            raise ValueError(f"Invalid stage {stage} for ScopeCommandGroup")

        if stage==Stage.Scope and has_subgroups:
            self.top: ScopeCommandGroup = ScopeCommandGroup(prober, Stage.Scope)
            self.bottom: ScopeCommandGroup = ScopeCommandGroup(prober, Stage.BottomScope)
            self.aux: ScopeCommandGroup = ScopeCommandGroup(prober, Stage.AuxiliaryScope)
        

    def move_xy(self, ref: XyReference, x: float, y: float) -> Tuple[float, float, XyReference]:
        """Move scope to a given position.

        Args:
            ref: The position reference for the submitted values.
            x: The x position in micrometer.
            y: The y position in micrometer.

        Returns:
            A tuple containing the x and y position after the move.
        """

        self.comm.send(f"scope:{self.__scope_selector}:move_xy {ref.to_string()},{x},{y}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), XyReference.from_string(tok[2])