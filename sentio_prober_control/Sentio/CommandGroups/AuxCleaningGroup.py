from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import ChuckSite


class AuxCleaningGroup(CommandGroupBase):
    """This command group provides functions for for cleaning the probe.
    You are not meant to create instances of this class on your own.
    Instead use the cleaning property of the AuxCommandGroup.

    Example:

    ```py
        from sentio_prober_control.Sentio.ProberSentio import SentioProber

        prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
        prober.aux.cleaning.enable_auto(True)
    ```

    """

    def enable_auto(self, stat: bool) -> None:
        """Enable automatic probe cleaning.

        Args:
            stat (bool): A flag indicating whether to enable or disable cleaning.
        """

        self.comm.send(f"aux:cleaning:enable_auto {stat}")
        Response.check_resp(self.comm.read_line())


    def reset_touch_counter(self, cs: ChuckSite) -> None:
        """Resets the touch counter of a cleaning pad

        Args:
            cs (ChuckSite): Enumerator defining the chuck site the cleaning pad is placed
        """

        self.comm.send(f"aux:cleaning:reset_touch_count {cs.toSentioAbbr()}")
        Response.check_resp(self.comm.read_line())


    def start(self, touchdowns: int | None = None) -> float:
        """Start the cleaning procedure.

        Args:
            touchdowns (int): The number of touchdowns to perform.
        """
        if touchdowns is None:
            self.comm.send(f"aux:cleaning:start")
        else:
            self.comm.send(f"aux:cleaning:start {touchdowns}")

        resp = Response.check_resp(self.comm.read_line())
        try:
            val = float(resp.message())
            return val
        except:
            return -1.0
