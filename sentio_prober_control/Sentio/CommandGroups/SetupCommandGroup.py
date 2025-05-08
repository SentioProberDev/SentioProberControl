from sentio_prober_control.Sentio.CommandGroups.SetupContactCounterCommandGroup import SetupContactCounterCommandGroup
from sentio_prober_control.Sentio.CommandGroups.SetupRemoteCommandGroup import SetupRemoteCommandGroup
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase


class SetupCommandGroup(ModuleCommandGroupBase):
    """A command group for accessing setup module functions."""
    def __init__(self, comm) -> None:
        super().__init__(comm, "setup")
        
        self.contact_counter: SetupContactCounterCommandGroup = SetupContactCounterCommandGroup(comm)
        self.remote: SetupRemoteCommandGroup = SetupRemoteCommandGroup(comm)