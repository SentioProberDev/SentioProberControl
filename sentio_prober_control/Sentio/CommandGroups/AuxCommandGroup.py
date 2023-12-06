from deprecated import deprecated

from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.CommandGroups.AuxCleaningGroup import  AuxCleaningGroup
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase

class AuxCommandGroup(ModuleCommandGroupBase):
    """ This command group contains functions for working with auxiliary sites of the chuck. 
        You are not meant to create instances of this class on your own. Instead use the aux property 
        of the SentioProber class.
        
        Attributes:
            cleaning (AuxCleaningGroup): A subgroup to provide logic for probe cleaning.
    """

    def __init__(self, comm):
        super().__init__(comm, 'aux')

        self.cleaning : AuxCleaningGroup = AuxCleaningGroup(comm)


    # Ticket #13774 Remove this function. It is already present in the cleaning group!
    @deprecated(reason="duplicated; Use the cleaning group instead.")
    def start_clean(self):
        self._comm.send("aux:cleaning:start")
        resp = Response.check_resp(self._comm.read_line())
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.message()

