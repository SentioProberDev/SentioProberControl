
from typing import Optional


from sentio_prober_control.Sentio.CommandGroups.StageCommandGroup import StageCommandGroup
from sentio_prober_control.Sentio.Compatibility import CompatibilityLevel, Compatibility
from sentio_prober_control.Sentio.Enumerations import Stage





class ScopeCommandGroup(StageCommandGroup):
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

    def __init__(self, prober: 'SentioProber', stage : Stage, stage_selector : str) -> None: # type: ignore
        super().__init__(prober, stage, stage_selector)

        if Compatibility.level >= CompatibilityLevel.Sentio_25_2:
            self.top : StageCommandGroup = StageCommandGroup(self, Stage.Scope, "scope:top")
            self.bottom : StageCommandGroup = StageCommandGroup(self, Stage.BottomScope, "scope:bottom")
            self.aux : StageCommandGroup = StageCommandGroup(self, Stage.AuxiliaryScope, "scope:aux")
