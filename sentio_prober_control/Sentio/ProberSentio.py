import base64
import os
from typing import Tuple
from enum import Enum

from deprecated import deprecated

from sentio_prober_control.Sentio.Enumerations import (
    ChuckSite,
    ChuckXYReference,
    ChuckThetaReference,
    ChuckZReference,
    DialogButtons,
    LoadPosition,
    ProjectFileInfo,
    Module,
    ScopeXYReference,
    ScopeZReference,
    Stage,
    SteppingContactMode,
    VceZReference,
    WorkArea
)

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
from sentio_prober_control.Sentio.Enumerations import ChuckSite


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

    def __init__(self, comm: CommunicatorBase):
        """Construct a SENTIO prober object.

        The prober must be initialized with a communication object that
        specifies how the system communicates with the probe station.

        Args:
            comm (CommunicatorBase): The communicator to use for communication with the prober.
        """
        ProberBase.__init__(self, comm)

        self.__name = "SentioProber"
        self.comm.send("*RCS 1")  # switch to the native SENTIO remote command set

        self.aux: AuxCommandGroup = AuxCommandGroup(self)
        self.compensation: CompensationCommandGroup = CompensationCommandGroup(self)
        self.loader: LoaderCommandGroup = LoaderCommandGroup(self)
        self.map: WafermapCommandGroup = WafermapCommandGroup(self)
        self.probe: ProbeCommandGroup = ProbeCommandGroup(self)
        self.qalibria: QAlibriaCommandGroup = QAlibriaCommandGroup(self)
        self.service: ServiceCommandGroup = ServiceCommandGroup(self)
        self.siph: SiPHCommandGroup = SiPHCommandGroup(self)
        self.status: StatusCommandGroup = StatusCommandGroup(self)
        self.vision: VisionCommandGroup = VisionCommandGroup(self)


    def abort_command(self, cmd_id: int) -> Response:
        """Stop an ongoing asynchronous remote command.

        Args:
            cmd_id (int): The id of the async command to abort.

        Returns:
            A response object with the result of the command.
        """
        self.comm.send("abort_command {0}".format(cmd_id))
        return Response.check_resp(self.comm.read_line())


    def clear_contact(self, site: ChuckSite | None = None) -> Response:
        """Clear contact positions.

        Args:
            site (ChuckSite): The chuck site to clear. If None is given all sites will be cleared.

        Returns:
            A response object with the result of the command.
        """

        if site is None:
            self.comm.send("clear_contact")
        else:
            self.comm.send(f"clear_contact {site.toSentioAbbr()}")

        return Response.check_resp(self.comm.read_line())


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
            return SentioProber(CommunicatorTcpIp.create(arg1))
        elif comm_type == "gpib" or comm_type == SentioCommunicationType.Gpib:
            return SentioProber(CommunicatorGpib.create(arg1, arg2))
        elif comm_type == "visa" or comm_type == SentioCommunicationType.Visa:
            return SentioProber(CommunicatorVisa.create(arg1))
        else:
            raise ValueError(f'Unknown prober type: "{comm_type}"')


    def enable_chuck_overtravel(self, stat: bool) -> Response:
        """Enable chuck overtravel.

        This function wraps SENTIO's "enable_chuck_overtravel" remote command.

        Args:
            stat (bool): True to enable, False to disable.

        Returns:
            A response object with the result of the command.
        """

        self.comm.send(f"enable_chuck_overtravel {stat}")
        return Response.check_resp(self.comm.read_line())


    def enable_chuck_hover(self, stat: bool) -> Response:
        """Enable chuck hover height.

        The Hover height is a height that is significantly closer to the chuck compared to the separation height.
        It is closer to the wafer but it is not safe for fast or long chuck moves as the chuck may be slightly
        tilted.

        This function wraps SENTIO's "enable_chuck_hover" remote command.

        Args:
            stat (bool): True to enable, False to disable.

        Returns:
            A response object with the result of the command.
        """

        self.comm.send(f"enable_chuck_hover {stat}")
        return Response.check_resp(self.comm.read_line())


    def enable_chuck_site_hover(self, site: ChuckSite, stat: bool) -> Response:
        """Enable chuck site hover height.

        The Hover height is a height that is significantly closer to the chuck compared to the separation height.
        It is closer to the wafer but it is not safe for fast or long chuck moves as the chuck may be slightly
        tilted.

        Args:
            site (ChuckSite): The chuck site to enable hover height for.
            stat (bool): True to enable, False to disable.

        Returns:
            A response object with the result of the command.
        """

        self.comm.send(f"enable_chuck_site_hover {site.toSentioAbbr()}, {stat}")
        return Response.check_resp(self.comm.read_line())


    def enable_chuck_site_overtravel(self, site: ChuckSite, stat: bool) -> Response:
        """Enable overtravel distance for a specific chuck site.

        Args:
            site (ChuckSite): The chuck site to enable overtravel distance for.
            stat (bool): True to enable, False to disable.

        Returns:
            A response object with the result of the command.
        """

        self.comm.send(f"enable_chuck_site_hover {site.toSentioAbbr()}, {stat}")
        return Response.check_resp(self.comm.read_line())


    def file_transfer(self, source: str, dest: str) -> Response:
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
        return Response.check_resp(self.comm.read_line())


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
        self.comm.send("get_chuck_site_heights {0}".format(site.toSentioAbbr()))
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
        self.comm.send("get_chuck_site_status {0}".format(site.toSentioAbbr()))
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

        self.comm.send("get_chuck_theta {0}".format(site.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_chuck_xy(self, site: ChuckSite, ref: ChuckXYReference) -> Tuple[float, float]:
        """Get current chuck xy position with respect to a given reference.

        Args:
            site (ChuckSite): The chuck site to query.
            ref (ChuckXYReference): The reference to use for the query.

        Returns:
            x (float): x position in micrometer.
            y (float): y position in micrometer.
        """

        if site is None:
            self.comm.send(f"get_chuck_xy {site.toSentioAbbr()}")
        else:
            self.comm.send(f"get_chuck_xy {site.toSentioAbbr()}, {ref.toSentioAbbr()}")

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


    def get_chuck_z(self, ref: ChuckZReference) -> float:
        """Get chuck z position.

        Args:
            ref (ChuckZReference): The reference to use for the query.

        Returns:
            height (float): The actual z position of the chuck in micrometer (from axis zero).
        """

        self.comm.send(f"get_chuck_z {ref.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def get_project(self, pfi: ProjectFileInfo = ProjectFileInfo.FullPath) -> str:
        """Get the name of the current project.

        Args:
            pfi (ProjectFileInfo): The type of information to get.

        Returns:
            project_name (str): The name of the current project.
        """

        self.comm.send(f"get_project {pfi.toSentioAbbr()}")
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

            This command queries the name and position of a scope site. The index is zero based.

        Args:
            idx (int): The index of the site to query.

        Returns:
            num (int): The number of defined scope sites.
        """

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


    def move_chuck_load(self, pos: LoadPosition) -> Response:
        """Move chuck to load position.

        Wraps SENTIO's "move_chuck_load" remote command.

        Args:
            pos (LoadPosition): The load position to move to.

        Returns:
            A response object with the result of the command.
        """
        self.comm.send("move_chuck_load {0}".format(pos.toSentioAbbr()))
        return Response.check_resp(self.comm.read_line())


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
        self.comm.send("move_chuck_site {0}".format(site.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2]), float(tok[3])


    def move_chuck_theta(self, ref: ChuckThetaReference, angle: float) -> float:
        """Move chuck theta axis to a given angle.

        Wraps SENTIO's "move_chuck_theta" remote command.

        Args:
            ref: The reference to use for the move.
            angle: The angle to move to in degrees.
        """
        self.comm.send("move_chuck_theta {0}, {1}".format(ref.toSentioAbbr(), angle))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_chuck_xy(self, ref: ChuckXYReference, x: float, y: float) -> Tuple[float, float]:
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
        self.comm.send("move_chuck_xy {0}, {1}, {2}".format(ref.toSentioAbbr(), x, y))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def move_chuck_z(self, ref: ChuckZReference, z: float) -> float:
        """Move chuck to a given z position.

        Wraps SENTIO's "move_chuck_z" remote command.

        Args:
            ref: The z-reference to use for the move.
            z: The z position to move to in micrometer.

        Returns:
            The actual z position in micrometer after the move.
        """
        self.comm.send("move_chuck_z {0}, {1}".format(ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_chuck_work_area(self, area: WorkArea) -> Response:
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
            A response object with the result of the command.
        """
        self.comm.send(f"move_chuck_work_area {area.toSentioAbbr()}")
        return Response.check_resp(self.comm.read_line())

    def move_scope_xy(
        self, ref: ScopeXYReference, x: float, y: float
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

        self.comm.send(f"move_scope_xy {ref.toSentioAbbr()}, {x}, {y}")
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

    def move_scope_z(self, ref: ScopeZReference, z: float) -> float:
        """Move scope to a given z position.

        Args:
            ref: The reference to use for the move.
            z: The z position to move to in micrometer.

        Returns:
            The actual z position in micrometer after the move.
        """
        self.comm.send("move_scope_z {0}, {1}".format(ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_vce_z(self, stage: Stage, ref: VceZReference, z: float) -> float:
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

        self.comm.send(f"move_vce_z {stage.toSentioAbbr()}, {ref.toSentioAbbr()}, {z}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def name(self) -> str:
        """Returns the name of the prober.

        Returns:
            This function will always return the string "SentioProber".
        """
        return self.__name

    def open_project(self, project: str, restore_heights: bool = False):
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


    def select_module(self, module: Module, tabSheet: str | None = None):
        """Activate a given SENTIO module.

        In response to this function SENTIO will switch its user interface to make
        the given module the active one.

        This function wraps the "select_module" remote command of SENTIO.

        Args:
            module: The module to activate.
            tabSheet: The name of the module tab to activate. If None is given the default tab will be activated.
        """
        if tabSheet is not None:
            self.comm.send(f"select_module {module.toSentioAbbr()}, {tabSheet}")
        else:
            self.comm.send(f"select_module {module.toSentioAbbr()}")

        Response.check_resp(self.comm.read_line())


    def send_cmd(self, cmd: str) -> Response:
        """Sends a command to the prober and return a response object.

        This function is intended for directly sending remote commands that
        are not yet included in the python wrapper. It will send the command
        and parse the respone from SENTIO.

        Do NOT send low level commands that do not have a response (i.e. "*LOCAL").
        This will lock the communication pipeline as it is waiting for a
        response that never arrives.

        It will then return a Response object with the extracted data from
        SENTIO's response.

        Returns:
            A response object with the result of the command.
        """
        self.comm.send(cmd)
        return Response.check_resp(self.comm.read_line())

    def set_chuck_site_height(
        self,
        site: ChuckSite,
        contact: float,
        separation: float,
        overtravel_dist: float,
        hover_gap: float,
    ) -> Response:
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
        """
        par: str = f"{site.toSentioAbbr()},{contact},{separation},{overtravel_dist},{hover_gap}"
        self.comm.send("set_chuck_site_heights {0}".format(par))
        return Response.check_resp(self.comm.read_line())


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

        self.comm.send(f"set_stepping_contact_mode {mode.toSentioAbbr()}")
        Response.check_resp(self.comm.read_line())


    def set_vacuum(self, site: ChuckSite, stat: bool) -> Response:
        """Switches the vacuum of a chuck site on or off.

        Args:
            site: The chuck site to switch the vacuum for.
            stat: True to switch the vacuum on, False to switch it off.

        Returns:
            A response object with the result of the command.
        """

        self.comm.send(f"set_vacuum {site.toSentioAbbr()}, {stat}")
        return Response.check_resp(self.comm.read_line())


    def show_hint(self, msg: str, subtext: str) -> Response:
        """Show an on screen message (hint) and return immediately

        Hints are on screen messages that pop up in SENTIO's lower left corner. This hint will
        disappears automatically after a few seconds.

        This function wraps SENTIO's "status:show_hint" remote command.

        Args:
            msg: The message to display.
            subtext: The subtext to display.
        """
        self.comm.send(f'status:show_hint "{msg}", "{subtext}"')
        return Response.check_resp(self.comm.read_line())


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
                msg, buttons.toSentioAbbr(), caption
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
