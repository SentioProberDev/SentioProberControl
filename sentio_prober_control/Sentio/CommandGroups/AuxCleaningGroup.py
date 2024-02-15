from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


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

    def enable_auto(self, stat: bool):
        """Enable automatic probe cleaning.

        Args:
            stat (bool): A flag indicating whether to enable or disable cleaning.
        """

        self._comm.send(f"aux:cleaning:enable_auto {stat}")
        Response.check_resp(self._comm.read_line())

    def start(self, touchdowns: int = None):
        """Start the cleaning procedure.

        Args:
            touchdowns (int): The number of touchdowns to perform.
        """
        if touchdowns is None:
            self._comm.send(f"aux:cleaning:start")
        else:
            self._comm.send(f"aux:cleaning:start {touchdowns}")

        resp = Response.check_resp(self._comm.read_line())
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.message()

