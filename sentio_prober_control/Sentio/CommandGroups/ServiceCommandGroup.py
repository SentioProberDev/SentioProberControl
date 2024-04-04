from sentio_prober_control.Sentio.Enumerations import SoftwareFence
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase


class ServiceCommandGroup(ModuleCommandGroupBase):
    """A command group for accessing service module functions."""

    def __init__(self, comm) -> None:
        super().__init__(comm, "service")


    def set_compensation_mode(self, status: bool) -> None:
        """Turn chuck compensation on or off.

        Args:
            status: True to turn on, False to turn off.

        Returns:
            A Response object.
        """

        self.comm.send(f"service:chuck_compensation {status}")
        Response.check_resp(self.comm.read_line())


    def set_software_fence(self, fence: SoftwareFence) -> None:
        """Set the software fence.

        The software fence is a virtual fence that is used to
        limit the movement of the chuck. The fences purpose
        is to prevent the chuck from moving into physical
        obstructions such as the machine casing or other
        hardware.

        Args:
            fence: The type of fence to use.

        Returns:
            A Response object.
        """

        self.comm.send(f"service:chuck_fence {fence.toSentioArg()}")
        Response.check_resp(self.comm.read_line())
