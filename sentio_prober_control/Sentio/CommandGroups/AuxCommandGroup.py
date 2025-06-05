from enum import Enum
from typing import Optional, Tuple, List
from dataclasses import dataclass

from sentio_prober_control.Sentio.Enumerations import ChuckSite, ElementType
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.CommandGroups.AuxCleaningGroup import AuxCleaningGroup
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase

class ElementInfoResponse:
    """
    A class to handle and parse the raw response string for element information 
    returned from SENTIO's "aux:get_element_info" command.

    Attributes:
        raw_response (str): The raw comma-separated response from SENTIO.
        element_info (ElementInfo): The parsed element information.
    """
    def __init__(self, raw_response: str) -> None:
        self.raw_response = raw_response
        parts = raw_response.split(",")
        if len(parts) < 7:
            raise ProberException("Unexpected response for element info.")

        # Parse the parts into an ElementInfo object.
        self.element_info = ElementInfo(
            element_type=ElementType.from_string(parts[0]),
            element_subtype=parts[1],
            x_position=float(parts[2]),
            y_position=float(parts[3]),
            spacing=float(parts[4]),
            touch_count=int(parts[5]),
            life_time=float(parts[6])
        )

    def get_element_info(self) -> "ElementInfo":
        """
        Returns:
            The parsed ElementInfo instance.
        """
        return self.element_info



@dataclass
class ElementInfo:
    element_type: ElementType
    element_subtype: str
    x_position: float
    y_position: float
    spacing: float
    touch_count: int
    life_time: float


class AuxCommandGroup(ModuleCommandGroupBase):
    """This command group contains functions for working with auxiliary sites of the chuck.
    You are not meant to create instances of this class on your own. Instead, use the aux
    property of the SentioProber class.

    Attributes:
        cleaning (AuxCleaningGroup): A subgroup to provide logic for probe cleaning.
    """

    def __init__(self, prober : 'SentioProber') -> None:
        super().__init__(prober, "aux")
        self.cleaning: AuxCleaningGroup = AuxCleaningGroup(prober)

    # --- Helper method to validate that the given site is an auxiliary site ---
    def _validate_aux_site(self, site: "ChuckSite") -> None:
        # Only auxiliary sites (e.g. AuxRight, AuxLeft, AuxRight2, AuxLeft2) are allowed.
        # Wafer and ChuckCamera are not valid for these commands.
        if site in (ChuckSite.Wafer, ChuckSite.ChuckCamera):
            raise ProberException(f"Invalid auxiliary site: {site.name}.")

    def retrieve_substrate_data(self, site: Optional["ChuckSite"] = None) -> List["ChuckSite"]:
        """
        Retrieves contact and home information from the configuration file and assigns it
        to the corresponding auxiliary site. Must be used after system start, since data
        are not retrieved automatically for safety reasons.

        Wraps SENTIO's "aux:retrieve_substrate_data" remote command.

        Args:
            site: (Optional) The auxiliary site (e.g. ChuckSite.AuxRight).
                  If omitted, data for all auxiliary sites is retrieved.

        Returns:
            A list of ChuckSite for which data was retrieved.
        """

        cmd = "aux:retrieve_substrate_data"
        if site:
            self._validate_aux_site(site)
            cmd += f" {site.to_string()}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        parts = resp.message().split(",")
        if not parts or len(parts) < 1:
            return []

        # The response format is "<count>,<site1>,<site2>,..."
        # Skip the count and convert each token to its corresponding ChuckSite.
        sites = []
        for token in parts[1:]:
            token = token.strip()
            for aux_site in ChuckSite:
                if token.lower() == aux_site.to_string().lower():
                    sites.append(aux_site)
                    break
        return sites

    def get_substrate_type(self, site: Optional["ChuckSite"] = None) -> str:
        """
        Retrieves the type of a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_substrate_type" remote command.

        Args:
            site: (Optional) The auxiliary site (e.g. ChuckSite.AuxRight).
                  If omitted, the currently active site is used.

        Returns:
            A string describing the substrate type.
            If the remote command returns "OK", an empty string is returned.
        """
        
        cmd = "aux:get_substrate_type"
        if site:
            self._validate_aux_site(site)
            cmd += f" {site.to_string()}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        substrate_type = resp.message()
        if substrate_type.upper() == "OK":
            return ""
        return substrate_type

    def step_to_element(
        self,
        element_standard_id: str,
        offset_x: float = 0.0,
        offset_y: float = 0.0,
        motorized_positioner_move: bool = True
    ) -> None:
        """
        Steps to a calibration element on the currently active chuck site.

        Wraps SENTIO's "aux:step_to_element" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            offset_x: An X offset (in micrometers).
            offset_y: A Y offset (in micrometers).
            motorized_positioner_move: If True, move with motorized positioner.
                                       If False, only chuck move.
        """
        cmd = (
            f"aux:step_to_element {element_standard_id},"
            f"{offset_x},{offset_y},{str(motorized_positioner_move).lower()}"
        )
        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def step_to_dut_element(
        self,
        dut_name: str,
        move_z: bool = True,
        x: Optional[float] = None,
        y: Optional[float] = None
    ) -> None:
        """
        Steps to a DUT element on the currently active chuck site.

        Wraps SENTIO's "aux:step_to_dut_element" remote command.

        Args:
            dut_name: The name of the DUT element (e.g. "RefDUT").
            move_z: If True, move Z automatically. If False, skip Z movement.
            x: (Optional) X position [um].
            y: (Optional) Y position [um].
        """
        cmd = f"aux:step_to_dut_element {dut_name},{str(move_z).lower()}"
        if x is not None and y is not None:
            cmd += f",{x},{y}"

        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def get_element_type(self, element_standard_id: str, site: Optional["ChuckSite"] = None) -> ElementType:
        """
        Retrieves the type of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_type" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) The auxiliary site (e.g. ChuckSite.AuxRight).
                  If omitted, the currently active site is used.

        Returns:
            An ElementType enumerator (e.g. ElementType.Short, ElementType.Thru, ElementType.Align, etc).
        """
        cmd = "aux:get_element_type"
        if site:
            self._validate_aux_site(site)
            cmd += f" {site.to_string()},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        result = resp.message()
        return ElementType.from_string(result)

    def get_substrate_info(self, site: "ChuckSite") -> Tuple[str, str, float]:
        """
        Retrieves information of a calibration substrate or cleaning pad placed on a chuck site.

        Wraps SENTIO's "aux:get_substrate_info" remote command.

        Args:
            site: The auxiliary site (e.g. ChuckSite.AuxRight).

        Returns:
            A tuple containing:
                - substrate_type (str)
                - substrate_id (str) [if the id is "OK", an empty string is returned]
                - life_time (float) in %
        """
        self._validate_aux_site(site)
        cmd = f"aux:get_substrate_info {site.to_string()}"
        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        parts = resp.message().split(",")
        if len(parts) < 3:
            raise ProberException("Unexpected response for get_substrate_info.")
        substrate_type = parts[0]
        substrate_id = parts[1]
        if substrate_id.upper() == "OK":
            substrate_id = ""
        life_time = float(parts[2])
        return (substrate_type, substrate_id, life_time)

    def get_element_touch_count(self, element_standard_id: str, site: Optional["ChuckSite"] = None) -> int:
        """
        Retrieves the touch count of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_touch_count" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) The auxiliary site (e.g. ChuckSite.AuxRight).
                  If omitted, the currently active site is used.

        Returns:
            The touch count (int) of the element.
        """
        cmd = "aux:get_element_touch_count"
        if site:
            self._validate_aux_site(site)
            cmd += f" {site.to_string()},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())

    # -------------------------------------------------------------------------
    # 8) get_element_spacing
    # -------------------------------------------------------------------------
    def get_element_spacing(self, element_standard_id: str, site: Optional["ChuckSite"] = None) -> float:
        """
        Retrieves the spacing value of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_spacing" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) The auxiliary site (e.g. ChuckSite.AuxRight).
                  If omitted, the currently active site is used.

        Returns:
            The spacing in micrometers (float).
        """
        cmd = "aux:get_element_spacing"
        if site:
            self._validate_aux_site(site)
            cmd += f" {site.to_string()},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    # -------------------------------------------------------------------------
    # 9) get_element_pos
    # -------------------------------------------------------------------------
    def get_element_pos(self, element_standard_id: str, site: Optional["ChuckSite"] = None) -> Tuple[float, float]:
        """
        Retrieves the (X, Y) position of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_pos" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) The auxiliary site (e.g. ChuckSite.AuxRight).
                  If omitted, the currently active site is used.

        Returns:
            A tuple (x_position, y_position) in micrometers (floats).
        """
        cmd = "aux:get_element_pos"
        if site:
            self._validate_aux_site(site)
            cmd += f" {site.to_string()},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        parts = resp.message().split(",")
        if len(parts) < 2:
            raise ProberException("Unexpected response for get_element_pos.")
        x = float(parts[0])
        y = float(parts[1])
        return (x, y)

    # -------------------------------------------------------------------------
    # 10) get_element_life_time
    # -------------------------------------------------------------------------
    def get_element_life_time(self, element_standard_id: str, site: Optional["ChuckSite"] = None) -> float:
        """
        Retrieves the life time (in %) of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_life_time" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) The auxiliary site (e.g. ChuckSite.AuxRight).
                  If omitted, the currently active site is used.

        Returns:
            The life time percentage (float).
        """
        cmd = "aux:get_element_life_time"
        if site:
            self._validate_aux_site(site)
            cmd += f" {site.to_string()},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    # -------------------------------------------------------------------------
    # 11) get_element_info
    # -------------------------------------------------------------------------
    def get_element_info(self, element_standard_id: str, site: Optional["ChuckSite"] = None) -> ElementInfo:
        """
        Retrieves information of a calibration element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_info" remote command.

        According to the SENTIO specification:
        - If a site is given, the command format is:
                aux:get_element_info <ChuckSite>,<ElementStandardID>
        - If no site is given, the command format is:
                aux:get_element_info <ElementStandardID>

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) The auxiliary site (e.g. ChuckSite.AuxRight).
                If omitted, the currently active site is used.

        Returns:
            An ElementInfo object containing:
                - element_type (ElementType)
                - element_subtype (str)
                - x_position (float)
                - y_position (float)
                - spacing (float)
                - touch_count (int)
                - life_time (float)
        """
        # Construct the command based on whether a site is specified
        cmd = "aux:get_element_info"
        if site is not None:
            self._validate_aux_site(site)
            # First parameter is the optional chuck site, second is the element ID
            cmd += f" {site.to_string()},{element_standard_id}"
        else:
            # Only the element ID is passed if the site is omitted
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        
        # Use the ElementInfoResponse class to parse the raw response
        parser = ElementInfoResponse(resp.message())
        return parser.get_element_info()