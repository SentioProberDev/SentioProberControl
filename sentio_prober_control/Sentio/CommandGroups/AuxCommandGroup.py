from typing import Optional, Tuple, List, Dict, Union
from deprecated import deprecated

from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.CommandGroups.AuxCleaningGroup import AuxCleaningGroup
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import (
    ModuleCommandGroupBase,
)

class AuxCommandGroup(ModuleCommandGroupBase):
    """This command group contains functions for working with auxiliary sites of the chuck.
    You are not meant to create instances of this class on your own. Instead, use the aux
    property of the SentioProber class.

    Attributes:
        cleaning (AuxCleaningGroup): A subgroup to provide logic for probe cleaning.
    """

    def __init__(self, comm) -> None:
        super().__init__(comm, "aux")
        self.cleaning: AuxCleaningGroup = AuxCleaningGroup(comm)

    # -------------------------------------------------------------------------
    #  1) retrieve_substrate_data
    # -------------------------------------------------------------------------
    def retrieve_substrate_data(self, site: Optional[str] = None) -> Tuple[int, List[str]]:
        """
        Retrieves contact and home information from configuration file and assigns it
        to the corresponding auxiliary site. Must be used after system start, since data
        are not retrieved automatically for safety reasons.

        Wraps SENTIO's "aux:retrieve_substrate_data" remote command.

        Args:
            site: (Optional) The name/index of the site (e.g. "AuxRight").
                  If omitted, data for all auxiliary sites is retrieved.

        Returns:
            A tuple of (count, site_list):
              - count: The number of sites data has been retrieved for
              - site_list: A list of site names for which data was retrieved
        """
        cmd = "aux:retrieve_substrate_data"
        if site:
            cmd += f" {site}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())

        # The response is typically "0,0,<count>,<site1>,<site2>,..."
        # resp.message() returns "<count>,<site1>,<site2>,..."
        parts = resp.message().split(",")
        if len(parts) == 0:
            return 0, []

        count = int(parts[0])
        site_list = parts[1:]
        return count, site_list

    # -------------------------------------------------------------------------
    #  2) get_substrate_type
    # -------------------------------------------------------------------------
    def get_substrate_type(self, site: Optional[str] = None) -> str:
        """
        Retrieves the type of a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_substrate_type" remote command.

        Args:
            site: (Optional) The site index or name (e.g. "0", "AuxRight").
                  If omitted, the currently active site is used.

        Returns:
            A string describing the substrate type (e.g. "AC-2", "Wafer", "Brush").
        """
        cmd = "aux:get_substrate_type"
        if site:
            cmd += f" {site}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    # -------------------------------------------------------------------------
    #  3) step_to_element
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    #  4) step_to_dut_element
    # -------------------------------------------------------------------------
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
        # The typical format is:
        #   aux:step_to_dut_element <dut_name>,<move_z>,<x>,<y>
        cmd = f"aux:step_to_dut_element {dut_name},{str(move_z).lower()}"
        if x is not None and y is not None:
            cmd += f",{x},{y}"

        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    # -------------------------------------------------------------------------
    #  5) get_element_type
    # -------------------------------------------------------------------------
    def get_element_type(
        self,
        element_standard_id: str,
        site: Optional[str] = None
    ) -> str:
        """
        Retrieves the type of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_type" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) Substrate type or chuck site (e.g. "AuxRight").
                  If omitted, the currently active site is used.

        Returns:
            The element type as a string (e.g. "Open", "Short", "Thru", "Align", etc.).
        """
        cmd = "aux:get_element_type"
        if site:
            cmd += f" {site},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    # -------------------------------------------------------------------------
    #  6) get_substrate_info
    # -------------------------------------------------------------------------
    def get_substrate_info(self, site: Union[int, str]) -> Dict[str, Union[str, float]]:
        """
        Retrieves information of a calibration substrate or cleaning pad placed on a chuck site.

        Wraps SENTIO's "aux:get_substrate_info" remote command.

        Args:
            site: The index (0,1,2,...) or name ("AuxRight", "AuxLeft", etc.) of the site.

        Returns:
            A dict with keys:
                "substrate_type" (str),
                "substrate_id"   (str),
                "life_time"      (float) in %
        """
        cmd = f"aux:get_substrate_info {site}"
        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())

        parts = resp.message().split(",")
        # Typically: <substrate_type>,<substrate_id>,<life_time>
        if len(parts) < 3:
            raise ProberException("Unexpected response for get_substrate_info.")

        return {
            "substrate_type": parts[0],
            "substrate_id": parts[1],
            "life_time": float(parts[2])
        }

    # -------------------------------------------------------------------------
    #  7) get_element_touch_count
    # -------------------------------------------------------------------------
    def get_element_touch_count(
        self,
        element_standard_id: str,
        site: Optional[str] = None
    ) -> int:
        """
        Retrieves the touch count of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_touch_count" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) Substrate type or chuck site (e.g. "AuxRight").
                  If omitted, the currently active site is used.

        Returns:
            The touch count (int) of the element.
        """
        cmd = "aux:get_element_touch_count"
        if site:
            cmd += f" {site},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())

    # -------------------------------------------------------------------------
    #  8) get_element_spacing
    # -------------------------------------------------------------------------
    def get_element_spacing(
        self,
        element_standard_id: str,
        site: Optional[str] = None
    ) -> float:
        """
        Retrieves the spacing value of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_spacing" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) Substrate type or chuck site (e.g. "AuxRight").
                  If omitted, the currently active site is used.

        Returns:
            The spacing in micrometers (float).
        """
        cmd = "aux:get_element_spacing"
        if site:
            cmd += f" {site},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    # -------------------------------------------------------------------------
    #  9) get_element_pos
    # -------------------------------------------------------------------------
    def get_element_pos(
        self,
        element_standard_id: str,
        site: Optional[str] = None
    ) -> Tuple[float, float]:
        """
        Retrieves the (X, Y) position of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_pos" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) Substrate type or chuck site (e.g. "AuxRight").
                  If omitted, the currently active site is used.

        Returns:
            A tuple (x_position, y_position) in micrometers (floats).
        """
        cmd = "aux:get_element_pos"
        if site:
            cmd += f" {site},{element_standard_id}"
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
    def get_element_life_time(
        self,
        element_standard_id: str,
        site: Optional[str] = None
    ) -> float:
        """
        Retrieves the life time (in %) of an element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_life_time" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) Substrate type or chuck site (e.g. "AuxRight").
                  If omitted, the currently active site is used.

        Returns:
            The life time percentage (float).
        """
        cmd = "aux:get_element_life_time"
        if site:
            cmd += f" {site},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    # -------------------------------------------------------------------------
    # 11) get_element_info
    # -------------------------------------------------------------------------
    def get_element_info(
        self,
        element_standard_id: str,
        site: Optional[str] = None
    ) -> Dict[str, Union[str, float, int]]:
        """
        Retrieves information of a calibration element on a calibration substrate placed on the chuck.

        Wraps SENTIO's "aux:get_element_info" remote command.

        Args:
            element_standard_id: The standard ID of the element (e.g. "0102").
            site: (Optional) Substrate type or chuck site (e.g. "AuxRight").
                  If omitted, the currently active site is used.

        Returns:
            A dictionary with keys:
                "element_type" (str)      -> e.g. "Thru", "Open", "Short", "Align", ...
                "element_subtype" (str)   -> e.g. "GSG"
                "x_position" (float)
                "y_position" (float)
                "spacing" (float)
                "touch_count" (int)
                "life_time" (float)       -> in %
        """
        cmd = "aux:get_element_info"
        if site:
            cmd += f" {site},{element_standard_id}"
        else:
            cmd += f" {element_standard_id}"

        self.comm.send(cmd)
        resp = Response.check_resp(self.comm.read_line())

        parts = resp.message().split(",")
        if len(parts) < 7:
            raise ProberException("Unexpected response for get_element_info.")

        return {
            "element_type": parts[0],
            "element_subtype": parts[1],
            "x_position": float(parts[2]),
            "y_position": float(parts[3]),
            "spacing": float(parts[4]),
            "touch_count": int(parts[5]),
            "life_time": float(parts[6])
        }
