from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import ProbeSentio
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class SiPHCommandGroup(CommandGroupBase):
    """This command group contains functions for working with SiPH applications.
    You are not meant to instantiate this class directly. Access it via the siph attribute
    of the [SentioProber](SentioProber.md) class.
    """

    def __init__(self, comm) -> None:
        super().__init__(comm)


    def fast_alignment(self) -> Response:
        """Perform fast fiber alignment."""

        self.comm.send("siph:fast_alignment")
        return Response.check_resp(self.comm.read_line())


    def get_cap_sensor(self) -> Tuple[float, float]:
        """Get the capacitance sensor value.

        :raises: ProberException if an error occured.
        :return: A tuple with the values from the capacity sensors of probe 1 and probe 2.
        """
        self.comm.send("siph:get_cap_sensor")
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_intensity(self) -> float:
        """Get the current intensity value.

        :raises: ProberException if an error occured.
        :returns: The intensity value.
        """

        self.comm.send("siph:get_intensity")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())


    def gradient_search(self) -> None:
        """Execute SiPh gradient search.

        :raises: ProberException if an error occured.
        """

        self.comm.send("siph:gradient_search")
        Response.check_resp(self.comm.read_line())


    def move_hover(self, probe: ProbeSentio) -> None:
        """Move SiPh probe to hover height.

        :param probe: The probe on which the SiPh probe is mounted.
        :raises: ProberException if an error occured.
        """

        self.comm.send(f"siph:move_hover {probe.toSentioAbbr()}")
        Response.check_resp(self.comm.read_line())


    def move_separation(self, probe: ProbeSentio) -> None:
        """Move SiPh probe to separation height.

        :param probe: The probe on which the SiPh probe is mounted.
        :raises: ProberException if an error occured.
        """

        self.comm.send(f"siph:move_separation {probe.toSentioAbbr()}")
        Response.check_resp(self.comm.read_line())
