from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import IMagProZReference
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class VisionIMagProCommandGroup(CommandGroupBase):
    """This command group contains functions for working with an IMag pro microscope.

    You are not meant to instantiate this class directly. Access it via the imagpro attribute
    of the vision attribute of the [SentioProber](SentioProber.md) class.
    """

    def __init__(self, comm) -> None:
        super().__init__(comm)


    def move_z(self, ref: IMagProZReference, pos: float) -> float:
        """Move imagpro's internal z-axis

        Args:
            ref: The position reference for the motion command.
            pos: The position to move to.

        Returns:
            The actual position of the z-axis after the move command.
        """

        #
        # the imag pro axis is showing hysteresis behavior. z position seems to be only
        # reproducable when the axis is moved from one of its endpoints! If you remove
        # the next three lines. The z-position will become very inaccurate!
        #
        # self.comm.send("vis:imagpro:move_z center, -1000")
        # Response.check_resp(self.comm.read_line())
        # time.sleep(0.5)

        self.comm.send("vis:imagpro:move_z {0}, {1}".format(ref.toSentioAbbr(), pos))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_z(self, ref: IMagProZReference) -> float:
        """Get the position od imagpro's internal axis.

        Args:
            ref: The position reference for the returned value.

        Returns:
            The position of the z-axis.
        """

        par: str = ref.toSentioAbbr()
        self.comm.send(f"vis:imagpro:get_z {par}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_xy_comp(self, imag_pro_z: float) -> Tuple[float, float]:
        """Get the xy compensation value for a certain z-position of imagpro's internal axis

        Args:
            imag_pro_z: The z-position of imagpro's internal axis.

        Returns:
            The xy compensation value
        """

        self.comm.send(f"vis:imagpro:get_xy_comp {imag_pro_z}")

        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])
