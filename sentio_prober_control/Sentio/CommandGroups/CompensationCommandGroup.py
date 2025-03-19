from deprecated import deprecated

from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.Enumerations import Compensation, ExecuteCompensation, OnTheFlyMode
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


@deprecated(reason="duplicated; This command group is already a subgroup of the vision command group.")
class CompensationCommandGroup(CommandGroupBase):
    """This command group contains functions for working with x,y and z compensation.

    This command group was marked deprecated on 2023-09-04. It will be removed in a future version.
    Use the SentioProber.vis.compensation group instead!
    """

    def __init__(self, comm) -> None:
        """@private"""
        super().__init__(comm)


    @deprecated(reason="Use prober.vis.compensation.set_compensation instead.")
    def set_compensation(self, comp: Compensation, enable: bool):
        """Enable or disable compensation for a given subsystem.

        This command was marked deprecated on 2023-09-04. It will be removed in a future version.
        Use the command in the visioncompensation group instead:

        >>> prober.vis.compensation.set_compensation(comp, enable)
        """

        self.comm.send(f"vis:compensation:enable {comp.toSentioAbbr()}, {enable}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], tok[1]


    @deprecated(reason="Use prober.vis.compensation.start_execute instead.")
    def execute_compensation(self, comp: ExecuteCompensation, mode: OnTheFlyMode):
        """Execute compensation.

        This command was marked deprecated on 2023-09-04. It will be removed in a future version.
        use prober.vis.compensation.start_execute instead.

        """
        self.comm.send(
            "vis:compensation:start_execute {},{}".format(
                comp.toSentioAbbr(), mode.toSentioAbbr()
            )
        )
        resp = Response.check_resp(self.comm.read_line())
        return resp
