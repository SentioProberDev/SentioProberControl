
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class SetupContactCounterCommandGroup(CommandGroupBase):
    """This command group bundles functions setting up the contact counter."""
    
    def __init__(self, prober : 'SentioProber') -> None:
        super().__init__(prober)

    def get(self) -> int:
        """ Retrieves the contact counter value.

        Returns:
            An integer representing the number of times the chuck moved into contact height,
            excluding moves on cleaning substrate.
        """
        self.comm.send("setup:contact_counter:get")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())

    def reset(self) -> None:
        """ Resets the contact counter. 
        
            Returns:
                None
        """
        self.comm.send("setup:contact_counter:reset")
        Response.check_resp(self.comm.read_line())
