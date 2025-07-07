from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import ProbePosition, XyReference, ZReference, ChuckSite, Stage
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Compatibility import Compatibility, CompatibilityLevel
from sentio_prober_control.Sentio.CommandGroups.StageCommandGroup import StageCommandGroup


class ProbeCommandGroup(CommandGroupBase):
    """This command group contains functions for working with motorized prober.
    You are not meant to instantiate this class directly. Access it via the probe attribute
    of the [SentioProber](SentioProber.md) class.

    Example:

    ```py
    from sentio_prober_control.Sentio.ProberSentio import SentioProber

    prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
    prober.probe.move_probe_xy(ProbePosition.East, XyReference.Current, 1000, 2000)
    ```
    """

    class _TopBottomPositionSelector:
        """ This is a dummy command group for providing access to top and bottom probes.
        """
        def __init__(self, prober: 'SentioProber', stage : Stage, stage_selector : str) -> None: # type: ignore
            self.east : StageCommandGroup = StageCommandGroup(prober, stage, f"{stage_selector}:east")
            self.west : StageCommandGroup = StageCommandGroup(prober, stage, f"{stage_selector}:west")
            self.north : StageCommandGroup = StageCommandGroup(prober, stage, f"{stage_selector}:north")
            self.south : StageCommandGroup = StageCommandGroup(prober, stage, f"{stage_selector}:south")
            self.northeast : StageCommandGroup = StageCommandGroup(prober, stage, f"{stage_selector}:northeast")
            self.northwest : StageCommandGroup = StageCommandGroup(prober, stage, f"{stage_selector}:northwest")
            self.southeast : StageCommandGroup = StageCommandGroup(prober, stage, f"{stage_selector}:southeast")
            self.southwest : StageCommandGroup = StageCommandGroup(prober, stage, f"{stage_selector}:southwest")


    def __init__(self, prober: 'SentioProber') -> None:
        super().__init__(prober)

        if Compatibility.level >= CompatibilityLevel.Sentio_25_2:
            self.top = self._TopBottomPositionSelector(prober, Stage.TopProbe, "probe:top")
            self.bottom = self._TopBottomPositionSelector(prober, Stage.BottomProbe, "probe:bottom")

            # Top probes are also available as east, west, north, south, northeast, northwest, southeast, southwest
            self.east = self.top.east
            self.west = self.top.west
            self.north = self.top.north
            self.south = self.top.south
            self.northeast = self.top.northeast
            self.northwest = self.top.northwest
            self.southeast = self.top.southeast
            self.southwest = self.top.southwest
       

    def async_step_probe_site(self, probe: ProbePosition, idx: int) -> int:
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

        self.comm.send(f"start_step_positioner_site {probe.to_string()},{idx}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.cmd_id()


    def async_step_probe_site_next(self, probe: ProbePosition) -> int:
        """Step to next probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to the next site. This is an asynchronous command
        use in conjunction with ProberSentio.wait_complete() or ProberSentio.query_command_status().

        Args:
            probe: The probe to step.

        Returns:
            The async command id of the command.
        """

        self.comm.send(f"start_step_positioner_site_next {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.cmd_id()


    def async_step_probe_site_first(self, probe: ProbePosition) -> int:
        """Step to first probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to the first site. This is an asynchronous command
        use in conjunction with ProberSentio.wait_complete() or ProberSentio.query_command_status().

        Args:
            probe: The probe to step.

        Returns:
            The async command id of the command.
        """

        self.comm.send(f"start_step_positioner_site_first {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.cmd_id()


    def get_probe_site(self, probe: ProbePosition, idx: int) -> Tuple[str, float, float, str]:
        """Get information for a probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command returns the data associated with a site.

        Args:
            probe: The probe to get the site for.

        Returns:
            A tuple containing the site index, position x, the position y in micrometer and the reference.
        """
        
        # This command was briefly removed and is not part of the SENTIO 24.0
        # release. It was reintroduced in 25.1.
        Compatibility.assert_min(CompatibilityLevel.Sentio_25_1)

        self.comm.send(f"get_positioner_site {probe.to_string()},{idx}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")

        return str(tok[0]), float(tok[1]), float(tok[2]), str(tok[3])


    def get_probe_site_number(self, probe: ProbePosition) -> int:
        """Returns the total number of probe sites set up.

        Each positioner can define n a number of predefined positions called "sites".
        This command returns the total number of sites.

        Returns:
            The total number of sites.
        """

        self.comm.send(f"get_positioner_site_num {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())


    def get_probe_xy(self, probe: ProbePosition, ref: XyReference) -> Tuple[float, float]:
        """Get probe xy position in micrometer.

        Args:
            probe: The probe to get the position for.
            ref: The position reference for the returned values.

        Returns:
            A tuple containing the x and y position in micrometer.
        """

        self.comm.send(f"get_positioner_xy {probe.to_string()},{ref.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_probe_z(self, probe: ProbePosition, ref: ZReference) -> float:
        """Get probe z position in micrometer.

        Args:
            probe: The probe to get the position for.
            ref: The position reference for the returned values.

        Returns:
            The z position in micrometer.
        """
        
        # Note: 
        # Even in Sentio 24.x the ref parameter is expected in long form! This is why we use 
        # CompatibilityLevel.Sentio_25_2 here.
        self.comm.send(f"get_positioner_z {probe.to_string()},{ref.to_string(CompatibilityLevel.Sentio_25_2)}")

        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_probe_contact(self, probe: ProbePosition) -> float:
        """Move a probe to its contact position.

        Args:
            probe: The probe to move.

        Returns:
            The z position after the move in micrometer (from zero).
        """

        self.comm.send(f"move_positioner_contact {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_probe_separation(self, probe: ProbePosition) -> float:
        """Move a probe to its separation position.

        Args:
            probe: The probe to move.

        Returns:
            The z position after the move in micrometer (from zero).
        """

        self.comm.send(f"move_positioner_separation {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_probe_lift(self, stage: Stage, probe: ProbePosition) -> float:
        """Move a probe to its lift position.

        Args:
            stage: The probe stage (TopProbe/BottomProbe).
            probe: The probe position.

        Returns:
            The z position after the move in micrometer (from zero).
        """
        if stage == Stage.TopProbe:
            pos = 'top'
        elif stage == Stage.BottomProbe:
            pos = 'bottom'
        else:
            raise ValueError("Stage must be a probe stage")

        self.comm.send(f"probe:{pos}:{probe.to_string().lower()}:move_lift")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_probe_home(self, probe: ProbePosition) -> Tuple[float, float]:
        """Move probe to its home position.

        Args:
            probe: The probe to move.

        Returns:
            A tuple containing the x and y position after the move.
        """

        self.comm.send(f"move_positioner_home {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_probe_xy(self, probe: ProbePosition, ref: XyReference, x: float, y: float) -> Tuple[float, float]:
        """Move probe to a given position.

        Args:
            probe: The probe to move.
            ref: The position reference for the submitted values.
            x: The x position in micrometer.
            y: The y position in micrometer.

        Returns:
            A tuple containing the x and y position after the move.
        """

        self.comm.send(f"move_positioner_xy {probe.to_string()},{ref.to_string()},{x},{y}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_probe_z(self, probe: ProbePosition, ref: ZReference, z: float) -> float:
        """Move probe to a given z position.

        Args:
            probe: The probe to move.
            ref: The position reference for the submitted values.
            z: The target z position in micrometer.

        Returns:
            The z position after the move in micrometer (from zero).
        """

        # Note:
        # Even in Sentio 24.x the ref parameter is expected in long form! This is why we use
        # CompatibilityLevel.Sentio_25_2 here.
        self.comm.send(f"move_positioner_z {probe.to_string()},{ref.to_string(CompatibilityLevel.Sentio_25_2)},{z}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def set_probe_contact(self, probe: ProbePosition, z: float | None = None) -> None:
        """Set contact position of a positioner.

        Args:
            probe: The probe to set contact height.
            z: The contact height in micrometer. If not specified, the current z position is used.
        """

        if z == None:
            self.comm.send(f"set_positioner_contact {probe.to_string()}")
        else:
            self.comm.send(f"set_positioner_contact {probe.to_string()},{z}")

        Response.check_resp(self.comm.read_line())


    def set_probe_home(self, probe: ProbePosition, site: ChuckSite | None = None, x: float | None = None, y: float | None = None) -> None:
        """Set home position of a probe.

        Args:
            probe: The probe to set home position.
            site: The chuck site to set the home position for. If None is specified the current site is used.
            x: The x position in micrometer. If not specified, the current x position is used.
            y: The y position in micrometer. If not specified, the current y position is used.
        """
        if site is None:
            self.comm.send(f"set_positioner_home {probe.to_string()}")
        elif x is not None and y is not None:
            self.comm.send(f"set_positioner_home {probe.to_string()},{site.to_string()},{x},{y}")
        else:
            raise ValueError("When site is specified, x and y must also be specified.")
        
        Response.check_resp(self.comm.read_line())


    def step_probe_site(self, probe: ProbePosition, idx: int) -> Tuple[str, float, float]:
        """Step to a specific probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to such a site.

        Args:
            probe: The probe to step.
            idx: The index of the site to step to.

        Returns:
            A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """

        self.comm.send(f"step_positioner_site {probe.to_string()},{idx}")

        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])


    def step_probe_site_first(self, probe: ProbePosition) -> Tuple[str, float, float]:
        """Step to the first probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to the first site.

        Args:
            probe: The probe to step.

        Returns:
            A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """

        self.comm.send(f"step_positioner_site_first {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])


    def step_probe_site_next(self, probe: ProbePosition) -> Tuple[str, float, float]:
        """Step to the next probe site.

        Each positioner can define n a number of predefined positions called "sites".
        This command initiates a step to the next site.

        Args:
            probe: The probe to step.

        Returns:
            A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """

        self.comm.send(f"step_positioner_site_next {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])

    def enable_probe_motor(self, probe: ProbePosition, status: bool) -> None:
        """Enable/Disable the probe motor.

        Probe with 3 motors will enable and disable by following behavior.

        Args:
            probe: The probe to action.
            status: Enable or disable status

        """
        self.comm.send(f"enable_positioner_motor {probe.to_string()},{status}")
        Response.check_resp(self.comm.read_line())

    def get_probe_status(self, probe: ProbePosition) -> str:
        """Obtain the status of probe.

        Command will return 4 probe status

        Args:
            probe: The probe to step.

        Returns:
            Status of positioner with 4 digits, 1st digit indicates the East Positioner, 2nd digit indicates West Positioner
            3rd digit indicates the North Positioner, 4th digit indicates the South Positioner.
        """

        self.comm.send(f"get_positioner_status {probe.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def set_probe_status(self, probe: ProbePosition, status: bool) -> None:
        """Enable/Disable the probe stage in the SENTIO.

        Enable/Disable the Probes in the SENTIO.

        Args:
            probe: The probe to action.
            status: Enable or disable status

        """
        self.comm.send(f"set_positioner_status {probe.to_string()},{status}")
        Response.check_resp(self.comm.read_line())

