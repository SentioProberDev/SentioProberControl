import base64
import os
import re
from typing import Tuple, Optional, Callable, TypeVar
from enum import Enum

from deprecated import deprecated

from sentio_prober_control.Sentio.Enumerations import (
    ChuckPositionHint,
    ChuckSite,
    ChuckSpeed,
    ThetaReference,
    DialogButtons,
    LoadPosition,
    Module,
    ProjectFileInfo,
    SoftContactState,
    Stage,
    SteppingContactMode,
    HighPowerAirState,
    UserCoordState,
    SwapBridgeSide,
    DevicePosition,
    VacuumState,
    WorkArea,
    XyReference,
    ZReference
)
from sentio_prober_control.Sentio.Compatibility import CompatibilityLevel, Compatibility
from sentio_prober_control.Sentio.ProberBase import ProberBase, ProberException
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase
from sentio_prober_control.Communication.CommunicatorGpib import CommunicatorGpib, GpibCardVendor
from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
from sentio_prober_control.Communication.CommunicatorVisa import CommunicatorVisa
from sentio_prober_control.Sentio.CommandGroups.AuxCommandGroup import AuxCommandGroup
from sentio_prober_control.Sentio.CommandGroups.CompensationCommandGroup import CompensationCommandGroup
from sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup import LoaderCommandGroup
from sentio_prober_control.Sentio.CommandGroups.ProbeCommandGroup import ProbeCommandGroup
from sentio_prober_control.Sentio.CommandGroups.QAlibriaCommandGroup import QAlibriaCommandGroup
from sentio_prober_control.Sentio.CommandGroups.ServiceCommandGroup import ServiceCommandGroup
from sentio_prober_control.Sentio.CommandGroups.SiPHCommandGroup import SiPHCommandGroup
from sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup import StatusCommandGroup
from sentio_prober_control.Sentio.CommandGroups.VisionCommandGroup import VisionCommandGroup
from sentio_prober_control.Sentio.CommandGroups.WafermapCommandGroup import WafermapCommandGroup
from sentio_prober_control.Sentio.CommandGroups.SetupCommandGroup import SetupCommandGroup
from sentio_prober_control.Sentio.CommandGroups.StageCommandGroup import StageCommandGroup
from sentio_prober_control.Sentio.CommandGroups.ScopeCommandGroup import ScopeCommandGroup


class SentioCommunicationType(Enum):
    """This enum defines different types of prober communication.

    Attributes:
        BackToContact (0): Chuck will move back to contact position after stepping.
        StepToSeparation (1): Chuck will move to separation position after stepping.
        LockContact (2): Chuck cannot step when at contact. You will have to manually move it away from its contact position before issuing the next step command.
    """

    TcpIp = 0
    Gpib = 1
    Visa = 2

  

class SentioProber(ProberBase):
    """This class represents the SENTIO probe station in python.
    It provides wrapper for most of the remote commands exposed by SENTIO.

    Attributes:
        aux (AuxCommandGroup): The aux command group provides access the the aux site modules functionality.
        loader (LoaderCommandGroup): The loader command group provides access to the loader modules functionality.
        map (WafermapCommandGroup): The wafermap command group provides access to the wafermap modules functionality.
        probe (ProbeCommandGroup): The probe command group provides access to the probe modules functionality.
        qalibria (QAlibriaCommandGroup): The qalibria command group provides access to the qalibria modules functionality.
        service (ServiceCommandGroup): The service command group provides access to the service modules functionality.
        siph (SiPHCommandGroup): The siph command group provides access to the SiPH modules functionality.
        status (StatusCommandGroup): The status command group provides access to the dashboard modules functionality. (formerly called status module)
        vision (VisionCommandGroup): The vision command group provides access to the vision modules functionality.
    """

    def __init__(self, comm: CommunicatorBase, compat_level : CompatibilityLevel = CompatibilityLevel.Auto) -> None:
        """Construct a SENTIO prober object.

        The prober must be initialized with a communication object that
        specifies how the system communicates with the probe station.

        Args:
            comm (CommunicatorBase): The communicator to use for communication with the prober.
            compat_level (CompatibilityLevel): The compatibility level to use. If CompatibilityLevel.Auto is set SENTIO is queried to figure the compatibility level out.
        """
        ProberBase.__init__(self, comm)

        # Standard command groups
        self.aux: AuxCommandGroup = AuxCommandGroup(self)
        self.loader: LoaderCommandGroup = LoaderCommandGroup(self)
        self.map: WafermapCommandGroup = WafermapCommandGroup(self)
        self.qalibria: QAlibriaCommandGroup = QAlibriaCommandGroup(self)
        self.service: ServiceCommandGroup = ServiceCommandGroup(self)
        self.siph: SiPHCommandGroup = SiPHCommandGroup(self)
        self.status: StatusCommandGroup = StatusCommandGroup(self)
        self.vision: VisionCommandGroup = VisionCommandGroup(self)
        self.setup: SetupCommandGroup = SetupCommandGroup(self)

        self.__name = "SentioProber"
        self.comm.send("*RCS 1")  # switch to the native SENTIO remote command set

        # If the compatibility Level is set to Auto, we will try to determine the compatibility level
        if compat_level == CompatibilityLevel.Auto:
            version : str = self.status.get_version()

            # Extract version string
            match = re.search(r"Version:\s*([\d\.]+)", version)
            if match:
                version = match.group(1)
                parts = version.split(".")
                major = int(parts[0]) if len(parts) > 0 else None
                minor = int(parts[1]) if len(parts) > 1 else None
                release = int(parts[2]) if len(parts) > 2 else None
                if major==25 and (minor==1 or (minor==0 and release==99)):
                    Compatibility.level = CompatibilityLevel.Sentio_25_1
                elif major==25 and (minor==2 or (minor==1 and release==99)):
                    Compatibility.level = CompatibilityLevel.Sentio_25_2
                else:
                    Compatibility.level = CompatibilityLevel.Sentio_24_0

        # make sure there is a valid compatibility level now
        assert Compatibility.level != CompatibilityLevel.Auto, "Compatibility level could not be determined. Please set it manually."

        #
        # More command groups not supported by all SENTIO versions.
        #
        
        # The probe command group has optional sub-groups for top and bottom 
        # probes. These are only available for Sentio > 25.2. Therefore 
        # this command group must be initialized after determining the 
        # compatibility level.
        self.probe: ProbeCommandGroup = ProbeCommandGroup(self)

        # Command groups for stages; Only available for Sentio > 25.2
        if Compatibility.level >= CompatibilityLevel.Sentio_25_2:
            self.scope: ScopeCommandGroup = ScopeCommandGroup(self, Stage.Scope, "scope:top")
            self.chuck: StageCommandGroup = StageCommandGroup(self, Stage.Chuck, "chuck")

        #
        # Deprecated command groups
        #
        # DO NOT USE THEM IN NEW CODE! They will be removed in the future!

        self.compensation: CompensationCommandGroup = CompensationCommandGroup(self)


    def abort_command(self, cmd_id: int) -> Response:
        """Stop an ongoing asynchronous remote command.

        Args:
            cmd_id (int): The id of the async command to abort.

        Returns:
            A response object with the result of the command.
        """
        self.comm.send(f"abort_command {cmd_id}")
        return Response.check_resp(self.comm.read_line())


    def clear_contact(self, chuckSite: Optional[ChuckSite] = None) -> None:
        """Clear contact positions.

        Args:
            chuckSite (ChuckSite): The chuck site to clear. If None is given all sites will be cleared.

        Returns:
            None
        """

        if chuckSite is None:
            self.comm.send("clear_contact")
        else:
            self.comm.send(f"clear_contact {chuckSite.to_string()}")

        Response.check_resp(self.comm.read_line())


    @staticmethod
    def create_prober(comm_type : str | SentioCommunicationType, arg1 : str | GpibCardVendor = "127.0.0.1:35555", arg2 : str = "") -> 'SentioProber':
        """ Create an instance of a SentioProber object that is bound to a certain communication method. Your choices of communication are tcpip, gpib and visa.
         
            Args:
                comm_type (str): The type of communication to use. Valid values are "tcpip", "gpib" and "visa".
                arg1 (object): For tcpip this is a single string specifying address and port 
                               like "127.0.0.1:35555". For visa this is the address of the device like "GPIB0::20::INSTR". For gpib two parameters are needed. 
                               The first one is the [type of driver/card](/Communication/GpibCardVendor) installed in the system, the second parameter is the address of the device like "GPIB0:20".
                arg2 (str): Only used for gpib communication. This is the GPIB address of the prober i.e. "GPIB0:20". 
         """
        
        
        if comm_type == "tcpip" or comm_type == SentioCommunicationType.TcpIp:
            if not isinstance(arg1, str):
                raise ValueError(f"Invalid argument for TCP/IP communication: {arg1}. Expected a string containing an ip address and a port number. i.e.: \"127.0.0.1:35555\".")
            
            return SentioProber(CommunicatorTcpIp.create(arg1))
        elif comm_type == "gpib" or comm_type == SentioCommunicationType.Gpib:
            if not isinstance(arg1, GpibCardVendor):
                raise ValueError(f"Invalid argument for gpib communication: {arg1}. Expected a GpibCardVendor specification (either NI or ADLINK).")

            return SentioProber(CommunicatorGpib.create(arg1, arg2))
        elif comm_type == "visa" or comm_type == SentioCommunicationType.Visa:
            if not isinstance(arg1, str):
                raise ValueError(f"Invalid argument for VISA communication: {arg1}. Expected a string containing a VISA resource identifier. i.e.: \"GPIB0::20::INSTR\".")

            return SentioProber(CommunicatorVisa.create(arg1))
        else:
            raise ValueError(f'Unknown prober type: "{comm_type}"')


    def enable_chuck_overtravel(self, stat: bool) -> None:

        """Enable chuck overtravel.

        This function wraps SENTIO's "enable_chuck_overtravel" remote command.

        Args:
            stat (bool): True to enable, False to disable.

        Returns:
            None
        """

        self.comm.send(f"enable_chuck_overtravel {stat}")
        Response.check_resp(self.comm.read_line())


    def enable_chuck_hover(self, stat: bool) -> None:

        """Enable chuck hover height.

        The Hover height is a height that is significantly closer to the chuck compared to the separation height.
        It is closer to the wafer but it is not safe for fast or long chuck moves as the chuck may be slightly
        tilted.

        This function wraps SENTIO's "enable_chuck_hover" remote command.

        Args:
            stat (bool): True to enable, False to disable.

        Returns:
            None
        """

        self.comm.send(f"enable_chuck_hover {stat}")
        Response.check_resp(self.comm.read_line())


    def enable_chuck_site_hover(self, site: ChuckSite, stat: bool) -> None:

        """Enable chuck site hover height.

        The Hover height is a height that is significantly closer to the chuck compared to the separation height.
        It is closer to the wafer but it is not safe for fast or long chuck moves as the chuck may be slightly
        tilted.

        Args:
            site (ChuckSite): The chuck site to enable hover height for.
            stat (bool): True to enable, False to disable.

        Returns:
            None
        """

        self.comm.send(f"enable_chuck_site_hover {site.to_string()}, {stat}")
        Response.check_resp(self.comm.read_line())


    def enable_chuck_site_overtravel(self, site: ChuckSite, stat: bool) -> None:

        """Enable overtravel distance for a specific chuck site.

        Args:
            site (ChuckSite): The chuck site to enable overtravel distance for.
            stat (bool): True to enable, False to disable.

        Returns:
            None
        """

        self.comm.send(f"enable_chuck_site_hover {site.to_string()}, {stat}")
        Response.check_resp(self.comm.read_line())


    def file_transfer(self, source: str, dest: str) -> None:

        """Transfer a file to the prober.

        This function will transfer a file to the prober. The file will be stored in the position specified by
        the dest argument. Transmission of the file may take some time.

        Args:
            source (str): The path to the file to transfer.
            dest (str): The destination path on the prober. Must be a complete path including file name. Make sure that SENTIO has write access to the given destination.
        """

        # open file and encode with base64
        if not os.path.isfile(source):
            raise ProberException(f"File {source} not found!")

        file_bytes = open(source, "rb").read()
        encoded = base64.b64encode(file_bytes).decode("ascii")

        self.comm.send(f"file_transfer {dest}, {encoded}")
        Response.check_resp(self.comm.read_line())


    def get_chuck_site_height(self, site: ChuckSite) -> Tuple[float, float, float, float]:

        """Retrieves height information of a chuck site

        Example:

            contact, separation, overtravel_dist, hover_gap = get_chuck_site_height(ChuckSite.Wafer)

        Gets for chuck site "Wafer" contact height, separation heights ,overtravel distance and hover height

        Args:
            site (ChuckSite): The chuck site to query.

        Returns:
            contact (float): contact height
            separation (float): separation gap
            overtravel_dist (float): overtravel distance
            hover_gap (float): hover gap
        """

        self.comm.send("get_chuck_site_heights {0}".format(site.to_string()))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")

        contact = float(tok[0])
        separation = float(tok[1])
        overtravel_gap = float(tok[2])
        hover_gap = float(tok[3])

        return contact, separation, overtravel_gap, hover_gap


    def get_chuck_site_status(self, site: ChuckSite) -> Tuple[bool, bool, bool, bool]:
        """Get status of a chuck site.

        Wraps SENTIO's "get_chuck_site_status" remote command.

        Args:
            site (ChuckSite): The chuck site to query.

        Returns:
            hasHome (bool): True if the chuck site has a home position.
            hasContact (bool): True if the chuck site has a contact position.
            overtravelActive (bool): True if the overtravel is active.
            vacuumOn (bool): True if the vacuum is on.
        """
        self.comm.send("get_chuck_site_status {0}".format(site.to_string()))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")

        def str_to_bool(v: str):
            if v == "0":
                return False
            elif v == "1":
                return True
            else:
                raise ProberException(f"get_chuck_site_status: Invalid boolean value ({v})")

        hasHome = str_to_bool(tok[0])
        hasContact = str_to_bool(tok[1])
        overtravelActive = str_to_bool(tok[2])
        vacuumOn = str_to_bool(tok[3])

        return hasHome, hasContact, overtravelActive, vacuumOn


    def get_chuck_theta(self, site: ChuckSite) -> float:
        """Get the current angle of the chuck.

        Wraps SENTIO's "get_chuck_theta" remote command.

        Args:
            site (ChuckSite): The chuck site to query.

        Raises:
            ProberException: If no available port is found.

        Returns:
            angle (float): The current angle of the chuck site in degrees.
        """

        self.comm.send("get_chuck_theta {0}".format(site.to_string()))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_chuck_xy(self, site: ChuckSite, ref: XyReference) -> Tuple[float, float]:
        """Get current chuck xy position with respect to a given reference.

        Args:
            site (ChuckSite): The chuck site to query.
            ref (XyReference): The reference to use for the query.

        Returns:
            x (float): x position in micrometer.
            y (float): y position in micrometer.
        """

        if site is None:
            self.comm.send(f"get_chuck_xy {site.to_string()}")
        else:
            self.comm.send(f"get_chuck_xy {site.to_string()}, {ref.to_string()}")

        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    @deprecated(reason="Duplicate functionality; Use get_chuck_xy instead")
    def get_chuck_xy_pos(self) -> Tuple[float, float]:
        self.comm.send("get_chuck_xy")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        curX = float(tok[0])
        curY = float(tok[1])
        return curX, curY


    def get_chuck_z(self, ref: ZReference) -> float:
        """Get chuck z position.

        Args:
            ref (ZReference): The reference to use for the query.

        Returns:
            height (float): The actual z position of the chuck in micrometer (from axis zero).
        """

        self.comm.send(f"get_chuck_z {ref.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def get_project(self, pfi: ProjectFileInfo = ProjectFileInfo.FullPath) -> str:
        """Get the name of the current project.

        Args:
            pfi (ProjectFileInfo): The type of information to get.

        Returns:
            project_name (str): The name of the current project.
        """

        self.comm.send(f"get_project {pfi.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def get_scope_xy(self) -> Tuple[float, float]:
        """Get current scope xy position.

        The returned position is an absolute position with respect to the axis zero in micrometer.

        Returns:
            x (float): The current x position in micrometer.
            y (float): The current y position in micrometer.
        """

        self.comm.send("get_scope_xy")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def get_scope_z(self) -> float:
        """Get scope z position in micrometer from axis zero.

        Returns:
            height (float): The z position in micrometer.
        """

        self.comm.send("get_scope_z")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_scope_site(self, idx : int) -> Tuple[str, float, float, bool]:
        """ Get scope site data.

            This command queries the name and position of a scope site. The index 
            is zero based.

        Args:
            idx (int): The index of the site to query.

        Returns:
            num (int): The number of defined scope sites.
        """

        # This command was briefly removed and is not part of the SENTIO 24.0
        # release. It was reintroduced in 25.2.
        Compatibility.assert_min(CompatibilityLevel.Sentio_25_2)

        self.comm.send(f"get_scope_site {idx}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")

        id = tok[0]
        x = float(tok[1])
        y = float(tok[2])

        # tok[3] is the reference which should always be "home"

        enabled = tok[4].upper() == "TRUE"

        return (id, x, y, enabled)
    

    def get_scope_site_num(self) -> int:
        """Get total number of scope sites.

        The scope stage can store a list of sites. Each site has a position and a name.
        This function returns the number of defined scope sites.

        Returns:
            num (int): The number of defined scope sites.
        """

        self.comm.send("get_scope_site_num")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())


    def has_chuck_xyz(self) -> bool:
        """Returns True if the chuck has xyz axes.

        Returns:
            has_xyz (bool): True if the chuck has xyz axes.
        """

        self.comm.send("has_chuck_xyz")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper() == "YES"


    def has_scope_xyz(self) -> bool:
        """Returns True if the scope has xyz axes.

        Returns:
            has_xyz (bool): True if the scope has xyz axes.
        """

        self.comm.send("has_scope_xyz")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper() == "YES"


    def has_scope_z(self) -> bool:
        """Returns true if the microscope has a motorized z axis.

        Returns:
            True if the scope has z axes.
        """

        self.comm.send("has_scope_z")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper() == "YES"


    def initialize_if_needed(self):
        """Initialize the prober if it is not already initialized.

        This command will check if the prober is already initialized. If not
        it will start the initialization process and wait for it to complete.

        You do not have to call waitcomplete after this function on your own!
        """
        isInitialized, isMeasuring, isLoaderBusy = self.status.get_machine_status()

        if not isInitialized:
            resp = self.start_initialization()

            if not resp.ok():
                raise ProberException(f"Cannot start initialization: {resp.message()}")

            resp = self.wait_complete(resp.cmd_id(), 180)
            if not resp.ok():
                raise ProberException(f"Initialization failed: {resp.message()}")


    def local_mode(self):
        """Switch the prober back into local mode.

        The probe station will automatically enter remote mode when a remote command is received.
        It will remian in remote mode even after the script is finished. This command can be used
        to switch the machine back into local mode and thus enable its UI.
        """
        self.comm.send("*LOCAL")

    T = TypeVar("T")
    def get(self, variable : str, stype: Callable[[str], T] = str) -> T:
        """Get a variable from the prober.

        This function wraps SENTIO's "*GET?" remote command.
        This command can query the value of any internal SENTIO variable that is accessible via the 
        SENTIO's internal environment object.

        Args:
            variable (str): The full name of the global variable to get.

        Returns:
            value (str): The value of the variable.
        """
        self.comm.send(f"*GET? {variable}")
        resp : str = self.comm.read_line()
        return stype(resp)


    def move_chuck_contact(self) -> float:
        """Move the chuck to contact height.

        Wraps SENTIO's "move_chuck_contact" remote command.

        Returns:
            height (float): The contact height in micrometer from chuck z axis zero.
        """

        self.comm.send("move_chuck_contact")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_chuck_home(self) -> Tuple[float, float]:
        """Move chuck to its home position.

        Returns:
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
        """

        self.comm.send("move_chuck_home ")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_chuck_load(self, pos: LoadPosition) -> None:
        """Move chuck to load position.

        Wraps SENTIO's "move_chuck_load" remote command.

        Args:
            pos (LoadPosition): The position to move the chuck to. This can either be a load position or the center position of the chuck.

        Returns:
            None
        """
        self.comm.send(f"move_chuck_load {pos.to_string()}")
        Response.check_resp(self.comm.read_line())


    def move_chuck_separation(self) -> float:
        """Move the chuck to separation height.

        Returns:
            The separation height in micrometer from chuck z axis zero.
        """
        self.comm.send("move_chuck_separation ")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_chuck_site(self, site: ChuckSite) -> Tuple[float, float, float, float]:
        """Moves chuck to the last active position of the selected chuck site.

        Wraps SENTIO's "move_chuck_site" remote command.

        Returns:
            x (float): The x position in micrometer.
            y (float): The y position in micrometer.
            z (float): The z height in micrometer.
            theta (float): The theta angle in degrees.
        """
        self.comm.send("move_chuck_site {0}".format(site.to_string()))
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2]), float(tok[3])


    def move_chuck_theta(self, ref: ThetaReference, angle: float) -> float:
        """Move chuck theta axis to a given angle.

        Wraps SENTIO's "move_chuck_theta" remote command.

        Args:
            ref: The reference to use for the move.
            angle: The angle to move to in degrees.
        """
        self.comm.send(f"move_chuck_theta {ref.to_string()}, {angle}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_chuck_xy(self, ref: XyReference, x: float, y: float) -> Tuple[float, float]:
        """Move chuck to a given xy position.

        Wraps SENTIO's "move_chuck_xy" remote command.

        Args:
            ref: The reference to use for the move.
            x: The x position to move to in micrometer.
            y: The y position to move to in micrometer.

        Returns:
            x: The chuck x position after the move in micrometer (from zero)
            y: The chuck y position after the move in micrometer (from zero)
        """
        self.comm.send(f"move_chuck_xy {ref.to_string()}, {x}, {y}")
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def move_chuck_z(self, ref: ZReference, z: float) -> float:
        """Move chuck to a given z position.

        Wraps SENTIO's "move_chuck_z" remote command.

        Args:
            ref: The z-reference to use for the move.
            z: The z position to move to in micrometer.

        Returns:
            The actual z position in micrometer after the move.
        """
        self.comm.send(f"move_chuck_z {ref.to_string()}, {z}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_chuck_work_area(self, area: WorkArea) -> None:
        """Move the chuck to a given work area.

        A SENTIO probe station can have different work areas. One area is for probing. This is the default
        work area and present on all probe stations. When the chuck is at probing position is is roughly
        centered with respect to the platen and located in a space were probes can go into contact.
        Depending on the machine type a prober may be equipped with a second work area. This
        area is located under an optional off-axis camera. The off-axis camera allows
        inspection of the wafer when the scope camera view is blocked by certain probe card types.

        This function wraps SENTIO's "move_chuck_work_area" remote command.

        Args:
            area: The work area to move to.

        Returns:
            None
        """
        self.comm.send(f"move_chuck_work_area {area.to_string()}")
        Response.check_resp(self.comm.read_line())

    def move_scope_xy(
        self, ref: XyReference, x: float, y: float
    ) -> Tuple[float, float]:
        """Move scope to a given xy position.

        Args:
            ref: The reference to use for the move.
            x: The x position to move to in micrometer.
            y: The y position to move to in micrometer.

        Returns:
            x: Scope x position after the move in micrometers (from zero)
            y: Scope x position after the move in micrometers (from zero)
        """

        self.comm.send(f"move_scope_xy {ref.to_string()}, {x}, {y}")
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def move_scope_lift(self, state: bool):
        """Move scope to its lift position.

        The scope lift position is a position where the scope is
        at its axis maximum. This position will give you the maximum
        possible are of unhindered operation when changing probe cards
        or other maintenance tasks.

        Args:
            state: True to move to the lift position, False to move away from the lift position.
        """
        self.comm.send(f"move_scope_lift {state}")
        Response.check_resp(self.comm.read_line())

    def move_scope_z(self, ref: ZReference, z: float) -> float:
        """Move scope to a given z position.

        Args:
            ref: The reference to use for the move.
            z: The z position to move to in micrometer.

        Returns:
            The actual z position in micrometer after the move.
        """
        self.comm.send(f"move_scope_z {ref.to_string()}, {z}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_vce_z(self, stage: Stage, ref: ZReference, z: float) -> float:
        """Move VCE stage to a given z position.

        Args:
            ref: The reference to use for the move.
            z: The z position to move to in micrometer.

        Returns:
            The actual z position in micrometer after the move.
        """
        if stage != Stage.Vce and stage != Stage.Vce2:
            raise ProberException(
                f"This command can only be applied to vce stages! (stage={0})"
            )

        self.comm.send(f"move_vce_z {stage.to_string()}, {ref.to_string()}, {z}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def name(self) -> str:
        """Returns the name of the prober.

        Returns:
            This function will always return the string "SentioProber".
        """
        return self.__name

    def open_project(self, project: str, restore_heights: bool = False) -> None:
        """Open a SENTIO project file.

        Wraps SENTIO's "open_project" remote command.

        Args:
            project: The name or path of the project to open. If a full
                     path to the trex project file is given SENTIO will try to open this file.
                     If the argument does not contain a path SENTIO will look in its default
                     project folder for a matching project and open it.
            restore_heights: If set to true SENTIO will restore the contact
                             heights from the project. Be carefull when using this option because
                             the contact heights may have been become invalid since creating the project
                             due to a probe card change.
        """
        self.comm.send(f"open_project {project}, {restore_heights}")
        Response.check_resp(self.comm.read_line())

    def query_command_status(self, cmd_id: int) -> Response:
        """Query the status of an async command.

        This command will send a query to the prober to get the status
        of an async command. The submitted command id must be a valid id
        of an async command that was previously started at the prober.

        When an async command is being executed SENTIO can receive other
        remnote commands. This command is intended to be used in a polling
        loop to query the status of ongoing remote commands.

        Example:

        <pre><code>while True:
            time.sleep(1)
            resp = prober.query_command_status(cmd_id)
            if (resp.errc()!=RemoteCommandError.CommandPending):
                break;</code></pre>

        Args:
            cmd_id: The id of the async command to query.

        Returns:
            A response object with the result of the command.
        """
        self.comm.send("query_command_status {0}".format(cmd_id))
        resp = Response.parse_resp(self.comm.read_line())
        return resp

    def save_config(self):
        """Save the SENTIO configuration file.

        Wraps SENTIO's "save_config" remote command.
        """
        self.comm.send("save_config")
        Response.check_resp(self.comm.read_line())

    def save_project(self, project: str):
        """Save the current SENTIO project.

        Wraps SENTIO's "save_project" remote command.
        """
        self.comm.send("save_project " + project)
        Response.check_resp(self.comm.read_line())


    def select_module(self, module: Module, tabSheet: str | None = None) -> None:
        """Activate a given SENTIO module.

        In response to this function SENTIO will switch its user interface to make
        the given module the active one.

        This function wraps the "select_module" remote command of SENTIO.

        Args:
            module: The module to activate.
            tabSheet: The name of the module tab to activate. If None is given the default tab will be activated.
        """
        if tabSheet is not None:
            self.comm.send(f"select_module {module.to_string()}, {tabSheet}")
        else:
            self.comm.send(f"select_module {module.to_string()}")

        Response.check_resp(self.comm.read_line())


    def send_cmd(self, cmd: str) -> Response:
        """Sends a command to the prober and return a response object.

        This function is intended for directly sending remote commands that
        are not yet included in the python wrapper. It will send the command
        and parse the respone from SENTIO.

        Support low level remote command.

        It will then return a Response object with the extracted data from
        SENTIO's response.

        Returns:
            A response object with the result of the command.
        """
    
        self.comm.send(cmd)
        
        if '*' in cmd and '?' in cmd:
            return Response(0,0,0,self.comm.read_line())

        elif '*' in cmd:
            return Response(0,0,0,"")
        
        else:
            return Response.check_resp(self.comm.read_line())

    def set_chuck_site_height(
        self,
        site: ChuckSite,
        contact: float,
        separation: float,
        overtravel_dist: float,
        hover_gap: float,
    ) -> Tuple[ChuckSite, float, float, float, float]:
        """Sets z position information of a chuck site

        Example:

            prober.set_chuck_site_height(ChuckSite.Wafer,16000,250,20,50)

        Will set the contact height of the wafer site to 16000 µm with a separation height of 250 µm an overtravel of 20 and a hover height of 50

        Args:
            site: The chuck site to query.
            contact: The new contact height in micrometer.
            separation: The new separation height in micrometer.
            overtravel_dist: The new overtravel distance in micrometer.
            hover_gap: The new hover gap in micrometer.

        Returns:
            site: The chuck site that was set.
            contact: The new contact height in micrometer.
            separation: The new separation height in micrometer.
            overtravel_dist: The new overtravel distance in micrometer.
            hover_gap: The new hover gap in micrometer.
        """

        self.comm.send(f"set_chuck_site_heights {site.to_string()},{contact},{separation},{overtravel_dist},{hover_gap}")
        resp = Response.check_resp(self.comm.read_line())        
        tok = resp.message().split(",")
        site = ChuckSite[tok[0]]
        contact = float(tok[1])
        separation = float(tok[2])
        overtravel_dist = float(tok[3])
        hover_gap = float(tok[4])

        return site, contact, separation, overtravel_dist, hover_gap


    def set_ink(self, idx_inker : int) -> None:
        """ Trigger the inker device.

            Wraps SENTIO's "set_ink" remote command.

        Args:
            idx_inker: The index of the inker to trigger. The index is one based (use either 1 or 2). 
        """

        self.comm.send(f"set_ink {idx_inker}")
        Response.check_resp(self.comm.read_line())


    def set_stepping_contact_mode(self, mode: SteppingContactMode) -> None:
        """Change the stepping contact mode.

        The stepping contact mode defines what happens during stepping over a wafer.
        The following modes are available:

        * BackToContact: The chuck will step into contact position
        * StepToSeparation: The chuck will step into separation position. You have to move into contact with a seaparate command.
        * LockContack: The Chuck is not allowed to leave contact position automatically as part of a stepping command. You have to move into separation with a separate command bevore being able to step to the next die..

        Args:
             mode: The stepping contact mode to set.
        """

        self.comm.send(f"set_stepping_contact_mode {mode.to_string()}")
        Response.check_resp(self.comm.read_line())


    def set_vacuum(self, site: ChuckSite, stat: bool) -> None:
        """Switches the vacuum of a chuck site on or off.

        Args:
            site: The chuck site to switch the vacuum for.
            stat: True to switch the vacuum on, False to switch it off.

        Returns:
            None
        """

        self.comm.send(f"set_vacuum {site.to_string()}, {stat}")
        Response.check_resp(self.comm.read_line())


    def show_hint(self, msg: str, subtext: str) -> None:
        """Show an on screen message (hint) and return immediately

        Hints are on screen messages that pop up in SENTIO's lower left corner. This hint will
        disappears automatically after a few seconds.

        This function wraps SENTIO's "status:show_hint" remote command.

        Args:
            msg: The message to display.
            subtext: The subtext to display.
        """
        self.comm.send(f'status:show_hint "{msg}", "{subtext}"')
        Response.check_resp(self.comm.read_line())


    def show_hint_and_wait(
        self,
        msg: str,
        subtext: str,
        button_caption: str,
        timeout: int = 180,
        lock_ui: bool = True,
    ) -> None:
        """Show an on screen message with a button wait for a button to be pressed.

        Hints pop up in SENTIO's lower left corner. This function will display a hint with a button
        and only return once the button has been pressed.

        Args:
            msg: The message to display.
            subtext: The subtext to display. Subtext is displayed in a second line with a slightly smaller font.
            button_caption: The caption of the button.
            timeout: An optional timeout in seconds after which the dialog will be closed automatically. (default = 180 s)
            lock_ui: An optional flag that determines wether the UI shall be locked. Most of the UI is disabled in
                     remote mode anyway. This button affects only the on screen interactions on the right side of the main
                     module view. (default = True)
        """

        self.comm.send(
            f'status:start_show_hint "{msg}", "{subtext}", "{button_caption}", "{lock_ui}"'
        )
        resp = Response.check_resp(self.comm.read_line())

        # wait for button press
        self.comm.send(f"wait_complete {resp.cmd_id()}, {timeout}")
        Response.check_resp(self.comm.read_line())


    def show_message(
        self, msg: str, buttons: DialogButtons, caption: str, dialog_timeout: int = 180
    ) -> DialogButtons:
        """Pop up a message dialog in SENTIO and wait for the result.

        Args:
            msg: The message to display.
            buttons: The buttons to display.
            caption: The caption of the message box.
            dialog_timeout: An optional dialog timeout in seconds after which the dialog will be closed automatically.

        Returns:
            The button that was as an DialogButtons enum value.
        """
        self.comm.send(
            "status:start_show_message {0}, {1}, {2}".format(
                msg, buttons.to_string(), caption
            )
        )
        resp = Response.check_resp(self.comm.read_line())

        # wait for button press
        self.comm.send("wait_complete {0}, {1}".format(resp.cmd_id(), dialog_timeout))
        resp = Response.check_resp(self.comm.read_line())

        if resp.message().lower() == "ok":
            return DialogButtons.Ok

        if resp.message().lower() == "yes":
            return DialogButtons.Yes

        if resp.message().lower() == "no":
            return DialogButtons.No

        if resp.message().lower() == "cancel":
            return DialogButtons.Cancel

        raise ProberException("Invalid dialog button return value")


    def start_initialization(self) -> Response:
        """Start the initialization of the probe station.

        This function will start the initialization of the prober. This is an
        async command that will return immediately.

        The initialization process will take some time to complete. Use
        waitcomplete to wait for the initialization to complete.
        """
        self.comm.send("start_initialization")
        return Response.check_resp(self.comm.read_line())


    def wait_all(self, timeout: int = 90) -> Response:
        """Wait until all async commands have finished.

        Args:
            timeout: The timeout in seconds.

        Returns:
            A response object with the result of the command.
        """
        self.comm.send(f"wait_all {timeout}")
        return Response.check_resp(self.comm.read_line())


    def wait_complete(self, id_or_resp: int | Response, timeout: int = 300) -> Response:
        """Wait for a single async command to complete.

        Args:
            cmd_id: The id of the async command to wait for.
            timeout: The timeout in seconds.

        Returns:
            A response object with the result of the command.
        """
        if isinstance(id_or_resp, Response):
            self.comm.send(f"wait_complete {id_or_resp.cmd_id()}, {timeout}")    
        else:
            self.comm.send(f"wait_complete {id_or_resp}, {timeout}")

        return Response.check_resp(self.comm.read_line())


    def get_scope_home(self) -> tuple[float, float]:

        """Gets the home position information for the scope stage.

        Returns:
            A tuple containing the X and Y home positions in micrometers.
        """

        self.comm.send("get_scope_home")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        home_x = float(tok[0])
        home_y = float(tok[1])
        return home_x, home_y


    def set_scope_home(self, home_x: Optional[float] = None, home_y: Optional[float] = None) -> None:

        """Sets the home position for the scope stage.

        Args:
            home_x: (Optional) The X-coordinate of the home position in micrometers.
            home_y: (Optional) The Y-coordinate of the home position in micrometers.

        Returns:
            A Response object indicating whether the command was successful.
        """

        if home_x is not None and home_y is not None:
            self.comm.send(f"set_scope_home {home_x},{home_y}")
        else:
            self.comm.send("set_scope_home")

        Response.check_resp(self.comm.read_line())


    def step_scope_site(self, site_index: int | str) -> tuple[str, float, float]:
        """Steps the scope to the indicated site and sets it as the current site.

        Args:
            site_index: The scope site index (zero-based) or its ID.

        Returns:
            A tuple containing:
                - Site ID (string): The identifier of the current scope site.
                - Offset X (float): The X offset relative to the scope home position.
                - Offset Y (float): The Y offset relative to the scope home position.
        """
        self.comm.send(f"step_scope_site {site_index}")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        site_id = tok[0]
        offset_x = float(tok[1])
        offset_y = float(tok[2])

        return site_id, offset_x, offset_y


    def step_scope_site_first(self) -> tuple[str, float, float]:
        """Steps the scope to the first site in the scope site list.

        Returns:
            A tuple containing:
                - Site ID (string): The identifier of the current scope site.
                - Offset X (float): The X offset relative to the scope home position.
                - Offset Y (float): The Y offset relative to the scope home position.
        """
        self.comm.send("step_scope_site_first")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        site_id = tok[0]
        offset_x = float(tok[1])
        offset_y = float(tok[2])

        return site_id, offset_x, offset_y

    def step_scope_site_next(self) -> tuple[str, float, float]:
        """Steps the scope to the next site and sets it as the current site.

        Returns:
            A tuple containing:
                - Site ID (string): The identifier of the current scope site.
                - Offset X (float): The X offset relative to the scope home position.
                - Offset Y (float): The Y offset relative to the scope home position.
        """
        self.comm.send("step_scope_site_next")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        site_id = tok[0]
        offset_x = float(tok[1])
        offset_y = float(tok[2])

        return site_id, offset_x, offset_y

    def get_chuck_position_hint(self) -> tuple[ChuckPositionHint, ChuckSite]:
        """Get a verbal representation of the current chuck position and the active site.

        Returns:
            position_hint (str): Describes the chuck's general position, e.g., "Probing", "FrontLoad", "SideLoad".
            site (str): The current chuck site, e.g., "Wafer", "AuxRight", "ChuckCameraLR", etc.
        """
        self.comm.send("get_chuck_position_hint")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        pos_hint_str = tok[0]
        site_str = tok[1]

        pos_hint = ChuckPositionHint.from_string(pos_hint_str)
        site = ChuckSite.from_string(site_str)

        return pos_hint, site

    def get_chuck_site_count(self) -> int:
        """Retrieve the number of chuck sites.

        Wraps SENTIO's "get_chuck_site_count" remote command.

        Returns:
            count (int): The number of chuck sites.
        """
        self.comm.send("get_chuck_site_count")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        count = int(tok[0])

        return count

    def get_chuck_site_index(self, name: Optional[str] = None) -> int:
        """Retrieve the index of a chuck site by name. If no name is provided, returns the index of the current site.

        Args:
            name (str, optional): The name of the chuck site. If None, the current site index is returned.

        Returns:
            index (int): The index of the chuck site.
        """
        if name is None:
            self.comm.send("get_chuck_site_index")
        else:
            self.comm.send(f"get_chuck_site_index {name}")

        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        index = int(tok[0])

        return index

    def get_chuck_site_name(self, index: Optional[int] = None) -> ChuckSite:
        """Retrieve the name of a chuck site. If no index is given, returns the current site's name.

        Args:
            index (int, optional): The index of the chuck site. If None, gets the name of the current site.

        Returns:
            site (ChuckSite): The name of the chuck site.
        """
        if index is None:
            self.comm.send("get_chuck_site_name")
        else:
            self.comm.send(f"get_chuck_site_name {index}")

        resp = Response.check_resp(self.comm.read_line())
        site : ChuckSite = ChuckSite.from_string(resp.message())
        
        return site

    def get_chuck_site_pos(self, site: Optional[ChuckSite] = None) -> tuple[float, float, float]:
        """Retrieve position information of a chuck site.

        Args:
            site (ChuckSite, optional): The chuck site to query. If None, uses the current active site.

        Returns:
            tuple[float, float, float]: (home_x, home_y, angle) in µm and degrees.
        """
        if site is not None:
            site_arg = site.to_string()
            self.comm.send(f"get_chuck_site_pos {site_arg}")
        else:
            self.comm.send("get_chuck_site_pos")

        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        home_x = float(tok[0])
        home_y = float(tok[1])
        angle = float(tok[2])
        return home_x, home_y, angle

    def get_chuck_speed(self) -> ChuckSpeed:
        """Retrieve the current chuck speed setting.

        Returns:
            ChuckSpeed: Enum representing current chuck speed.
        """
        self.comm.send("get_chuck_speed")
        resp = Response.check_resp(self.comm.read_line())
        speed_str = resp.message().split(",")[0]

        speed = ChuckSpeed.from_string(speed_str)

        return speed

    def get_vacuum_status(self, site: ChuckSite | None = None) -> VacuumState:
        """Get the vacuum status of a chuck site.

        Args:
            site (ChuckSite, optional): The chuck site to query. If None, queries the currently active site.

        Returns:
            VacuumState: Enum indicating On or Off.
        """
        if site is not None:
            site_arg = site.to_string()
            self.comm.send(f"get_vacuum_status {site_arg}")
        else:
            self.comm.send("get_vacuum_status")

        resp = Response.check_resp(self.comm.read_line())
        status = resp.message().split(",")[0]

        return VacuumState.from_string(status)
    
    def get_wafer_diameter(self) -> float:
        """Get the diameter of wafer on chuck.

        Wraps SENTIO's "get_wafer_diameter" remote command.

        Returns:
            diameter (float): The wafer diameter in mm.
        """

        self.comm.send("get_wafer_diameter")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_chuck_hover(self) -> float:
        """Move the chuck to hover height.

        If hover height is not enabled, the move will not be carried out.

        Returns:
            z (float): The new Z position in micrometers with respect to zero.
        """
        self.comm.send("move_chuck_hover")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        z_pos = float(tok[0])

        return z_pos

    def move_chuck_index(self, ref: str, x_steps: int, y_steps: int) -> tuple[float, float]:
        """Move chuck xy by a number of index steps relative to a reference point.

        If the chuck is above separation height, it will move to separation before and return after movement.

        Args:
            ref (str): The reference point ("Zero", "Home", "Relative", "Center"). Case-insensitive.
            x_steps (int): Number of steps in X direction.
            y_steps (int): Number of steps in Y direction.

        Returns:
            new_x (float): New X position (in µm, from axis zero).
            new_y (float): New Y position (in µm, from axis zero).
        """
        self.comm.send(f"move_chuck_index {ref}, {x_steps}, {y_steps}")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        new_x = float(tok[0])
        new_y = float(tok[1])

        return new_x, new_y

    def move_chuck_lift(self) -> float:
        """Move chuck to "Lift" position.

        Wraps SENTIO's "move_chuck_lift" remote command.

        Returns:
            Height (float): The chuck Z position in µm.
        """

        self.comm.send("move_chuck_lift")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_chuck_xyt(self, x_offset: float, y_offset: float, theta_offset: float) -> None:
        """Move chuck xy and theta to match pattern to field of view center.

        If chuck is above separation height, it will move to separation first and stay there after movement.

        Args:
            x_offset (float): Offset in X direction (in µm).
            y_offset (float): Offset in Y direction (in µm).
            theta_offset (float): Offset in theta (in degrees).

        Returns:
            None
        """
        self.comm.send(f"move_chuck_xyt {x_offset}, {y_offset}, {theta_offset}")
        Response.check_resp(self.comm.read_line())

    def set_chuck_overtravel_gap(self, gap: float) -> None:
        """Set overtravel gap for all chuck sites.

        Args:
            gap (float): The overtravel gap in micrometers.

        Returns:
            None
        """
        self.comm.send(f"set_chuck_overtravel_gap {gap}")
        Response.check_resp(self.comm.read_line())

    def set_chuck_separation_gap(self, gap: float) -> None:
        """Set separation gap for all chuck sites.

        Args:
            gap (float): The separation gap in micrometers.

        Returns:
            None
        """
        self.comm.send(f"set_chuck_separation_gap {gap}")
        Response.check_resp(self.comm.read_line())


    def set_chuck_site_overtravel_gap(self, site: ChuckSite, gap: float) -> None:
        """Set overtravel gap for a specific chuck site.

        Args:
            site (ChuckSite): The chuck site to apply the overtravel gap to. Cannot be None.
            gap (float): Overtravel gap in micrometers.

        Raises:
            ValueError: If site is None.
        """
        if site is None:
            raise ValueError("site is required and cannot be None")

        site_arg = site.to_string()
        self.comm.send(f"set_chuck_site_overtravel_gap {site_arg}, {gap}")
        Response.check_resp(self.comm.read_line())

    def set_chuck_site_pos(
            self,
            x: float | None = None,
            y: float | None = None,
            theta: float | None = None,
            site: ChuckSite | None = None
    ) -> None:
        """Set home position information of a chuck site.

        Args:
            x (float, optional): Home X position in µm.
            y (float, optional): Home Y position in µm.
            theta (float, optional): Home angle in degrees.
            site (ChuckSite, optional): Site enum. If None, uses current chuck site.

        Returns:
            None
        """
        if x is not None and y is not None and theta is not None:
            site_arg = site.to_string() if site is not None else None

            if site_arg:
                self.comm.send(f"set_chuck_site_pos {site_arg},{x},{y},{theta}")
            else:
                self.comm.send(f"set_chuck_site_pos {x},{y},{theta}")
        else:
            self.comm.send("set_chuck_site_pos")

        Response.check_resp(self.comm.read_line())

    def set_chuck_site_separation_gap(self, site: ChuckSite, gap: float) -> None:
        """Set separation gap for a specific chuck site.

        Args:
            site (ChuckSite): The chuck site to apply the gap to. This parameter is required.
            gap (float): Separation gap in micrometers.

        Raises:
            ValueError: If site is None.
        """
        if site is None:
            raise ValueError("site is required and cannot be None")

        site_arg = site.to_string()
        self.comm.send(f"set_chuck_site_separation_gap {site_arg}, {gap}")
        Response.check_resp(self.comm.read_line())

    def set_high_power_air(self, state: HighPowerAirState) -> None:
        """Switch the air of high power prober card on or off.

        Args:
            state (HighPowerAirState): Enum value indicating whether to enable or disable air.

        Raises:
            ValueError: If state is None or not a valid enum.
        """
        if state is None:
            raise ValueError("state is required and must be a valid HighPowerAirState enum")

        self.comm.send(f"set_high_power_air {state.to_string()}")
        Response.check_resp(self.comm.read_line())

    def set_soft_contact(self, state: SoftContactState) -> None:
        """Enable or disable soft contact mode.

        Args:
            state (SoftContactState): Enum indicating whether to enable or disable soft contact.

        Raises:
            ValueError: If state is None.
        """
        if state is None:
            raise ValueError("state is required and must be a valid SoftContactState enum")

        self.comm.send(f"set_soft_contact {state.to_string()}")
        Response.check_resp(self.comm.read_line())

    def set_user_coordinate_origin(self, state: UserCoordState, x: float, y: float) -> None:
        """Set the new user coordinate origin (X, Y) for chuck or scope.

        Args:
            state (UserCoordState): Either UserCoordState.Chuck or UserCoordState.Scope.
            x (float): X offset in micrometers.
            y (float): Y offset in micrometers.

        Raises:
            ValueError: If any parameter is invalid.
        """
        if state is None:
            raise ValueError("state is required and must be a valid UserCoordState")

        cmd = f"set_user_coordinate_origin {state.to_string()},{x},{y}"
        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def create_project(self, path_or_name: str) -> str:
        """Create a new project. Overwrites if a project with the same name exists.

        Args:
            path_or_name (str): Full path or project name.
                                If only a name is given, it will be created in the default project directory.

        Returns:
            full_path (str): The full path to the created project file (*.trex).
        """
        self.comm.send(f"create_project {path_or_name}")
        resp = Response.check_resp(self.comm.read_line())

        # Parse response message
        tok = resp.message().split(",")
        full_path = tok[0]

        return full_path
    
    def get_indexer_pos(self) -> Tuple[int, str]:
        """Get currently indexer position.

        Returns:
            Tuple[int, str]: Indexer location (1~5), and indexer z-position ("up" or "down").
        """
        self.comm.send("get_indexer_pos")
        resp = Response.check_resp(self.comm.read_line())
        location, position = resp.message().split(",")
        return int(location), position

    def indexer_cda(self, on: bool) -> None:
        """Turn indexer CDA on or off.

        Args:
            on (bool): True to turn on, False to turn off.

        Returns:
            Response: Result response.
        """
        state = "on" if on else "off"
        self.comm.send(f"indexer_cda {state}")
        Response.check_resp(self.comm.read_line())

    def move_bottom_platen_contact(self) -> float:
        """Move bottom platen to contact height.

        Returns:
            float: New Z position in µm with respect to zero.
        """
        self.comm.send("move_bottom_platen_contact")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_bottom_platen_separation(self) -> float:
        """Move bottom platen to separation height.

        Returns:
            float: New Z position in µm with respect to zero.
        """
        self.comm.send("move_bottom_platen_separation")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_indexer_lift(self) -> None:
        """Move indexer up.

        Returns:
            None
        """
        self.comm.send("move_indexer_lift")
        Response.check_resp(self.comm.read_line())

    def move_indexer_down(self) -> None:
        """Move indexer down.

        Returns:
            None
        """
        self.comm.send("move_indexer_down")
        Response.check_resp(self.comm.read_line())

    def probe_air_lift(self, valve: str, position: str) -> None:
        """Control probe air lift mechanism.

        Args:
            valve (str): v1/v2
            position (str): lift or unlift

        Returns:
            None
        """
        self.comm.send(f"probe_air_lift {valve},{position}")
        Response.check_resp(self.comm.read_line())

    def set_signal_tower(self, red: int, yellow: int, green: int, blue: int) -> None:
        """Set signal tower LED states.

        Args:
            red (int): -1=no change, 0=off, 1=on, 2=blinking
            yellow (int)
            green (int)
            blue (int)

        Returns:
            None
        """
        self.comm.send(f"set_signal_tower {red},{yellow},{green},{blue}")
        Response.check_resp(self.comm.read_line())

    def set_signal_tower_buzzer(self, state: int) -> None:
        """Set signal tower buzzer state.

        Args:
            state (int): -1=no change, 0=off, 1=on, 2=pulsed

        Returns:
            Response: None
        """
        self.comm.send(f"set_signal_tower_buzzer {state}")
        Response.check_resp(self.comm.read_line())

    def start_move_indexer_pos(self, pos: int) -> None:
        """Asynchronously move indexer to position.

        Args:
            pos (int): Position index from 1 to 5

        Returns:
            None
        """
        self.comm.send(f"start_move_indexer_pos {pos}")
        Response.check_resp(self.comm.read_line())

    def swap_bridge(self, side: SwapBridgeSide, device_position: DevicePosition, delaytime: int = 8) -> None:
        """Control swap bridge side,position and delay time.

        Args:
            side (str): right/left/current
            device_position (str, optional): up/down
            delaytime (int) : 8
        Returns:
            None
        """
        cmd = f"swap_bridge {side}"
        if device_position:
            cmd += f",{device_position}"
        cmd += f",{delaytime}"
        self.comm.send(cmd)
        Response.check_resp(self.comm.read_line())

    def get_door_status(self, door: str) -> Tuple[bool, bool]:
        """Retrieves the closed and locked state of a door.

        Args:
            door (str): The door to query ("prober" or "loader").

        Returns:
            Tuple[bool, bool]: (is_closed, is_locked)
        """
        self.comm.send(f"get_door_status {door.lower()}")
        resp = Response.check_resp(self.comm.read_line())
        closed, locked = resp.message().split(",")
        return closed == "1", locked == "1"

    def set_door_lock(self, door: str, lock: bool) -> None:
        """Locks or unlocks the specified door.

        Args:
            door (str): The door to control ("prober" or "loader").
            lock (bool): True to lock the door, False to unlock.

        Returns:
            Response: Result of the operation.
        """
        state = "1" if lock else "0"
        self.comm.send(f"set_door_lock {door.lower()},{state}")
        Response.check_resp(self.comm.read_line())
