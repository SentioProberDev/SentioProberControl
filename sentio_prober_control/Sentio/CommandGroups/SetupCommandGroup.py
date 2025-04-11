from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import ThermoChuckState
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import (
    ModuleCommandGroupBase,
)


class SetupCommandGroup(ModuleCommandGroupBase):
    """A command group for accessing setup module functions."""
    def __init__(self, comm) -> None:
        super().__init__(comm, "setup")

    def get_contact_counter(self) -> int:
        """Retrieves the contact counter value.

        Returns:
            An integer representing the number of times the chuck moved into contact height,
            excluding moves on cleaning substrate.
        """
        self.comm.send("setup:contact_counter:get")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())

    def reset_contact_counter(self) -> None:
        """Resets the contact counter."""
        self.comm.send("setup:contact_counter:reset")
        Response.check_resp(self.comm.read_line())

    def remote_light_off_at_contact(self, status: bool) -> str:
        """Defines whether light is switched off at contact height in remote mode.

        Args:
            status (BooleanStatus): True/False, ON/OFF as defined in Enum.

        Returns:
            Response: Response object for result checking.
        """
        self.comm.send(f"setup:remote:light_off_at_contact {status}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def remote_light_on_at_separation(self, status: bool) -> str:
        """Defines whether light is switched on at separation height in remote mode.

        Args:
            status (BooleanStatus): True/False, ON/OFF as defined in Enum.

        Returns:
            Response: Response object for result checking.
        """
        self.comm.send(f"setup:remote:light_on_at_separation {status}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def remote_scope_follow_off(self, status: bool) -> str:
        """Defines whether scope follow mode is switched off in remote mode.

        Args:
            status (BooleanStatus): True/False, ON/OFF as defined in Enum.
                Note: ON disables scope follow.

        Returns:
            Response: Response object for result checking.
        """
        self.comm.send(f"setup:remote:scope_follow_off {status}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
