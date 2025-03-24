from typing import Tuple

from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase
from sentio_prober_control.Sentio.Enumerations import ProbeSentio, ProbeXYReference, ProbeZReference, ChuckSite
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class ProbeCommandGroup(CommandGroupBase):
    """This command group contains functions for working with motorized prober.
    You are not meant to instantiate this class directly. Access it via the probe attribute
    of the [SentioProber](SentioProber.md) class.

    Example:

    ```py
    from sentio_prober_control.Sentio.ProberSentio import SentioProber

    prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
    prober.probe.move_probe_xy(ProbeSentio.East, ProbeXYReference.Current, 1000, 2000)
    ```
    """

    def __init__(self, comm: CommunicatorBase) -> None:
        super().__init__(comm)


    def async_step_probe_site(self, probe: ProbeSentio, idx: int) -> int:
        """Start the process of stepping to a positioner site.

        Each positioner can define n a number of predefined positions called "sites". This command
        initiates a step to such a site. This is an asynchronous command use in conjunction with
        ProberSentio.wait_complete() or ProberSentio.query_command_status().

        Args:
            probe: The probe to step.
            idx: The index of the site to step to.

        Returns:
            The async command id of the command.
        """

        self.comm.send(f"start_step_positioner_site {probe.toSentioAbbr()},{idx}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.cmd_id()


    def async_step_probe_site_next(self, probe: ProbeSentio) -> int:
        """Step to next probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to the next site. This is an asynchronous command
        use in conjunction with ProberSentio.wait_complete() or ProberSentio.query_command_status().

        Args:
            probe: The probe to step.

        Returns:
            The async command id of the command.
        """

        self.comm.send(f"start_step_positioner_site_next {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.cmd_id()


    def async_step_probe_site_first(self, probe: ProbeSentio) -> int:
        """Step to first probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to the first site. This is an asynchronous command
        use in conjunction with ProberSentio.wait_complete() or ProberSentio.query_command_status().

        Args:
            probe: The probe to step.

        Returns:
            The async command id of the command.
        """

        self.comm.send(f"start_step_positioner_site_first {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.cmd_id()


    def get_probe_site(self, probe: ProbeSentio, idx: int) -> Tuple[int, float, float, str]:
        """Get information for a probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command returns the data associated with a site.

        Args:
            probe: The probe to get the site for.

        Returns:
            A tuple containing the site index, position x, the position y in micrometer and the reference.
        """
        self.comm.send(f"get_positioner_site {probe.toSentioAbbr()},{idx}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")

        return str(tok[0]), float(tok[1]), float(tok[2]), str(tok[3])


    def get_probe_site_number(self, probe: ProbeSentio) -> int:
        """Returns the total number of probe sites set up.

        Each positioner can define n a number of predefined positions called "sites".
        This command returns the total number of sites.

        Returns:
            The total number of sites.
        """

        self.comm.send(f"get_positioner_site_num {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())


    def get_probe_xy(self, probe: ProbeSentio, ref: ProbeXYReference) -> Tuple[float, float]:
        """Get probe xy position in micrometer.

        Args:
            probe: The probe to get the position for.
            ref: The position reference for the returned values.

        Returns:
            A tuple containing the x and y position in micrometer.
        """

        self.comm.send(f"get_positioner_xy {probe.toSentioAbbr()},{ref.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_probe_z(self, probe: ProbeSentio, ref: ProbeZReference) -> float:
        """Get probe z position in micrometer.

        Args:
            probe: The probe to get the position for.
            ref: The position reference for the returned values.

        Returns:
            The z position in micrometer.
        """
        self.comm.send(f"get_positioner_z {probe.toSentioAbbr()},{ref.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_probe_contact(self, probe: ProbeSentio) -> float:
        """Move a probe to its contact position.

        Args:
            probe: The probe to move.

        Returns:
            The z position after the move in micrometer (from zero).
        """

        self.comm.send(f"move_positioner_contact {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_probe_separation(self, probe: ProbeSentio) -> float:
        """Move a probe to its separation position.

        Args:
            probe: The probe to move.

        Returns:
            The z position after the move in micrometer (from zero).
        """

        self.comm.send(f"move_positioner_separation {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_probe_home(self, probe: ProbeSentio) -> Tuple[float, float]:
        """Move probe to its home position.

        Args:
            probe: The probe to move.

        Returns:
            A tuple containing the x and y position after the move.
        """

        self.comm.send(f"move_positioner_home {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_probe_xy(self, probe: ProbeSentio, ref: ProbeXYReference, x: float, y: float) -> Tuple[float, float]:
        """Move probe to a given position.

        Args:
            probe: The probe to move.
            ref: The position reference for the submitted values.
            x: The x position in micrometer.
            y: The y position in micrometer.

        Returns:
            A tuple containing the x and y position after the move.
        """

        self.comm.send(f"move_positioner_xy {probe.toSentioAbbr()},{ref.toSentioAbbr()},{x},{y}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_probe_z(self, probe: ProbeSentio, ref: ProbeZReference, z: float) -> float:
        """Move probe to a given z position.

        Args:
            probe: The probe to move.
            ref: The position reference for the submitted values.
            z: The target z position in micrometer.

        Returns:
            The z position after the move in micrometer (from zero).
        """

        self.comm.send(f"move_positioner_z {probe.toSentioAbbr()},{ref.toSentioAbbr()},{z}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def set_probe_contact(self, probe: ProbeSentio, z: float | None = None) -> None:
        """Set contact position of a positioner.

        Args:
            probe: The probe to set contact height.
            z: The contact height in micrometer. If not specified, the current z position is used.
        """

        if z == None:
            self.comm.send(f"set_positioner_contact {probe.toSentioAbbr()}")
        else:
            self.comm.send(f"set_positioner_contact {probe.toSentioAbbr()},{z}")

        Response.check_resp(self.comm.read_line())


    def set_probe_home(self, probe: ProbeSentio, site: ChuckSite | None = None, x: float | None = None, y: float | None = None) -> None:
        """Set home position of a probe.

        Args:
            probe: The probe to set home position.
            site: The chuck site to set the home position for. If None is specified the current site is used.
            x: The x position in micrometer. If not specified, the current x position is used.
            y: The y position in micrometer. If not specified, the current y position is used.
        """
        if site is None:
            self.comm.send(f"set_positioner_home {probe.toSentioAbbr()}")
        else:
            self.comm.send(f"set_positioner_home {probe.toSentioAbbr()},{site.toSentioAbbr()},{x},{y}")

        Response.check_resp(self.comm.read_line())


    def step_probe_site(self, probe: ProbeSentio, idx: int) -> Tuple[str, float, float]:
        """Step to a specific probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to such a site.

        Args:
            probe: The probe to step.
            idx: The index of the site to step to.

        Returns:
            A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """

        self.comm.send(f"step_positioner_site {probe.toSentioAbbr()},{idx}")

        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])


    def step_probe_site_first(self, probe: ProbeSentio) -> Tuple[str, float, float]:
        """Step to the first probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to the first site.

        Args:
            probe: The probe to step.

        Returns:
            A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """

        self.comm.send(f"step_positioner_site_first {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])


    def step_probe_site_next(self, probe: ProbeSentio) -> Tuple[str, float, float]:
        """Step to the next probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to the next site.

        Args:
            probe: The probe to step.

        Returns:
            A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """

        self.comm.send(f"step_positioner_site_next {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])

    def enable_probe_motor(self, probe: ProbeSentio, status: bool) -> None:
        """Enable/Disable the probe motor.

        Probe with 3 motors will enable and disable by following behavior.

        Args:
            probe: The probe to action.
            status: Enable or disable status

        """
        self.comm.send(f"enable_positioner_motor {probe.toSentioAbbr()},{status}")
        Response.check_resp(self.comm.read_line())

    def get_probe_status(self, probe: ProbeSentio) -> str:
        """Obtain the status of probe.

        Command will return 4 probe status

        Args:
            probe: The probe to step.

        Returns:
            Status of positioner with 4 digits, 1st digit indicates the East Positioner, 2nd digit indicates West Positioner
            3rd digit indicates the North Positioner, 4rd digit indicates the South Positioner.
        """

        self.comm.send(f"get_positioner_status {probe.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def set_probe_status(self, probe: ProbeSentio, status: bool) -> None:
        """Enable/Disable the probe stage in the SENTIO.

        Enable/Disable the Probes in the SENTIO.

        Args:
            probe: The probe to action.
            status: Enable or disable status

        """
        self.comm.send(f"set_positioner_status {probe.toSentioAbbr()},{status}")
        Response.check_resp(self.comm.read_line())

