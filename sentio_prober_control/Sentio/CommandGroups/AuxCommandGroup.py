from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *
from sentio_prober_control.Sentio.CommandGroups.AuxCleaningGroup import  AuxCleaningGroup
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase

class AuxCommandGroup(ModuleCommandGroupBase):
    """ This command group contains functions for working with auxiliary sites of the chuck. """

    def __init__(self, comm):
        """ Create a new instance of AuxCommandGroup. 
            @private
        """

        super().__init__(comm, 'aux')

        self.cleaning : AuxCleaningGroup = AuxCleaningGroup(comm)
        """ A subgroup to provide logic for probe cleaning. """

    # Ticket #13774 Remove this function. It is already present in the cleaning group!
    def start_clean(self):
        
        self._comm.send("aux:cleaning:start")
        resp = Response.check_resp(self._comm.read_line())
        if not resp.ok():
            raise ProberException(resp.message())

        return resp.message()

