from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import XyReference, ZReference, Stage, ChuckSite
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase

from typing import Optional


class StageCommandGroup(CommandGroupBase):
    """This command group contains functions for working with motorized stages.
    You are not meant to instantiate this class directly. Access it via the probe attribute
    of the [SentioProber](SentioProber.md) class.

    Example:

    ```py
    from sentio_prober_control.Sentio.ProberSentio import SentioProber

    prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
    prober.scope.move_probe_xy(XyReference.Current, 1000, 2000)
    ```
    """

    def __init__(self, prober: 'SentioProber', stage : Stage, stage_selector : str) -> None: # type: ignore
        super().__init__(prober)

        self.__stage = stage
        self.__stage_selector = stage_selector


    def get_home(self, chuck_site : ChuckSite = ChuckSite.Wafer) -> Tuple[float, float, ChuckSite]:
        """Retrieves index coordinates of the home die.

        Returns:
            Row and column index of the home die.
        """
        self.comm.send(f"{self.__stage_selector}:get_home {chuck_site.to_string()}")
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), ChuckSite.from_string(tok[2])


    def get_site(self, site_idx : int) -> Tuple[str, float, float, XyReference, bool]:
        """Returns the number of stage specific site position.

        Returns:
            id (str): The site identifier.
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
            ref (XyReference): The position reference for the returned values.
            enabled (bool): True if the site is enabled, False otherwise.
        """
        self.comm.send(f"{self.__stage_selector}:get_site {site_idx}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0],float(tok[1]), float(tok[2]), XyReference.from_string(tok[3]), bool(tok[4])


    def get_site_num(self) -> int:
        """Returns the number of stage specific site position.

        Returns:
            site_num (int): An integer number of sites for the stage.
        """
        self.comm.send(f"{self.__stage_selector}:get_site_num")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())


    def get_xy(self, ref_xy : XyReference) -> Tuple[float, float, XyReference]:
        """ Returns the stage position for a given reference.

        Returns:
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
            ref (XyReference): The position reference for the returned values.
        """
        self.comm.send(f"{self.__stage_selector}:get_xy {ref_xy.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), XyReference.from_string(tok[2])


    def get_z(self, ref_z : ZReference) -> Tuple[float, ZReference]:
        """Returns stage z-position.

        Returns:
            z (float): The x position in micrometer.
            ref (XyReference): The position reference for the returned values.
        """
        self.comm.send(f"{self.__stage_selector}:get_z {ref_z.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), ZReference.from_string(tok[1])


    def has_xy(self) -> bool:
        """Returns true if stage has an xy drive.

        Returns:
            has_xy_drive (bool): True is the stage has a motorized xy drive.
        """
        self.comm.send(f"{self.__stage_selector}:has_xy")
        resp = Response.check_resp(self.comm.read_line())
        return bool(resp.message())


    def has_z(self) -> bool:
        """Returns true if stage has an z drive.

        Returns:
            has_z_drive (bool): True is the stage has a motorized z drive.
        """
        self.comm.send(f"{self.__stage_selector}:has_z")
        resp = Response.check_resp(self.comm.read_line())
        return bool(resp.message())


    def lift(self, lift : bool) -> None:
        """Move stage to lift position.
        
        Returns:
            None
        """
        self.comm.send(f"{self.__stage_selector}:lift {lift}")
        Response.check_resp(self.comm.read_line())


    def move_xy(self, ref: XyReference, x: float, y: float) -> Tuple[float, float, XyReference]:
        """Move stage to a given position.

        Args:
            ref: The position reference for the submitted values.
            x: The x position in micrometer.
            y: The y position in micrometer.

        Returns:
            xpos (float): The x-position
            ypos (float): The y-position
            ref (XyReference): The position reference for the returned values.
        """

        self.comm.send(f"{self.__stage_selector}:move_xy {ref.to_string()},{x},{y}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), XyReference.from_string(tok[2])
    

    def move_z(self, ref: ZReference, z: float) -> Tuple[float, ZReference]:
        """Move stage to a given z position.

        Args:
            ref: The position reference for the submitted values.
            z: The z position in micrometer.

        Returns:
            zpos (float): The z-position 
            ref (ZReference): The position reference for the returned values.
        """

        self.comm.send(f"{self.__stage_selector}:move_z {ref.to_string()},{z}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), ZReference.from_string(tok[1])
    

    def set_home(self, x: Optional[float] = None, y: Optional[float] = None, site: Optional[ChuckSite] = None) -> Tuple[float, float, ChuckSite]:
        """ Set the stage home position.

        Args:
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
            site (ChuckSite): The chuck site to set the home position for.

        Returns:
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
            site (ChuckSite): The chuck site the home position was set for.
        """
        if (x is None and y is not None) or (y is None and x is not None):
            raise ValueError("If y is specified, x must also be specified (and vice versa).")

        args : str = f"{x},{y}" if x is not None and y is not None else ""
        args += f" {site.to_string()}" if site is not None else ""
        self.comm.send(f"{self.__stage_selector}:set_home {args}")

        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]),float(tok[1]),ChuckSite.from_string(tok[2])
    

    def step_site(self, site: str | int) -> Tuple[str, float, float]:
        """Step to a specific site.

        Args:
            site_idx (str|int): The index or identifier of the site to step to.

        Returns:
            id (str): The site identifier.
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
        """

        self.comm.send(f"{self.__stage_selector}:step_site {site}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0],float(tok[1]),float(tok[2])


    def step_site_first(self) -> Tuple[str, float, float]:
        """Step to the first site.

        Returns:
            id (str): The site identifier.
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
        """
        
        self.comm.send(f"{self.__stage_selector}:step_site_first")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0],float(tok[1]),float(tok[2])


    def step_site_next(self) -> Tuple[str, float, float]:
        """Step to the first site.

        Returns:
            id (str): The site identifier.
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
        """
        
        self.comm.send(f"{self.__stage_selector}:step_site_next")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return tok[0],float(tok[1]),float(tok[2])


    @property
    def stage(self) -> Stage:
        """The stage this command group is for."""
        return self.__stage
    



