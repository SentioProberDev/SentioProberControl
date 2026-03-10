
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.Enumerations import Compensation, ExecuteCompensation, OnTheFlyMode
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class CompensationCommandGroup(CommandGroupBase):
    """This command group contains functions for working with x,y and z compensation.

        !!! danger "Deprecated since 2023-09-04"
        This command group will be removed in a future version. 
        Use the SentioProber.vis.compensation group instead!
    """

    def __init__(self, prober : 'SentioProber') -> None: # type: ignore
        """@private"""
        super().__init__(prober)


    def set_compensation(self, comp: Compensation, enable: bool):
        """Enable or disable compensation for a given subsystem.

        !!! danger "Deprecated since 2023-09-04"
        This command group will be removed in a future version.
        Use the SentioProber.vis.compensation group instead!

        >>> prober.vis.compensation.set_compensation(comp, enable)
        """

        self.comm.send(f"vis:compensation:enable {comp.to_string()}, {enable}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], tok[1]


    def execute_compensation(self, comp: ExecuteCompensation, mode: OnTheFlyMode):
        """Execute compensation.

        !!! danger "Deprecated since 2023-09-04"
        This command group will be removed in a future version.
        use prober.vis.compensation.start_execute instead.

        """
        self.comm.send(
            "vis:compensation:start_execute {},{}".format(
                comp.to_string(), mode.to_string()
            )
        )
        resp = Response.check_resp(self.comm.read_line())
        return resp
