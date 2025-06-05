
from sentio_prober_control.Sentio.CommandGroups.SetupContactCounterCommandGroup import SetupContactCounterCommandGroup
from sentio_prober_control.Sentio.CommandGroups.SetupRemoteCommandGroup import SetupRemoteCommandGroup
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase


class SetupCommandGroup(ModuleCommandGroupBase):
    """A command group for accessing setup module functions."""
    def __init__(self, prober : 'SentioProber') -> None:
        super().__init__(prober, "setup")
        
        self.contact_counter: SetupContactCounterCommandGroup = SetupContactCounterCommandGroup(prober)
        self.remote: SetupRemoteCommandGroup = SetupRemoteCommandGroup(prober)