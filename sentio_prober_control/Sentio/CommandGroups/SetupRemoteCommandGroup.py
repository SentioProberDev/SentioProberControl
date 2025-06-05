
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase

class SetupRemoteCommandGroup(CommandGroupBase):
    """ This command group bundles functions setting up the behavior of SENTIO in remote mode. """
    def __init__(self, prober : 'SentioProber') -> None:
        super().__init__(prober)

    def light_off_at_contact(self, status: bool) -> None:
        """Defines whether light is switched off at contact height in remote mode.

        Args:
            status (BooleanStatus): True/False, ON/OFF as defined in Enum.

        Returns:
            None
        """
        self.comm.send(f"setup:remote:light_off_at_contact {status}")
        Response.check_resp(self.comm.read_line())
                
    def light_on_at_separation(self, status: bool) -> None:
        """Defines whether light is switched on at separation height in remote mode.

        Args:
            status (BooleanStatus): True/False, ON/OFF as defined in Enum.

        Returns:
            None
        """
        self.comm.send(f"setup:remote:light_on_at_separation {status}")
        Response.check_resp(self.comm.read_line())
        
    def scope_follow_off(self, status: bool) -> None:
        """Defines whether scope follow mode is switched off in remote mode.

        Args:
            status (BooleanStatus): True/False, ON/OFF as defined in Enum.
                Note: ON disables scope follow.

        Returns:
            Response: Response object for result checking.
        """
        self.comm.send(f"setup:remote:scope_follow_off {status}")
        Response.check_resp(self.comm.read_line())
