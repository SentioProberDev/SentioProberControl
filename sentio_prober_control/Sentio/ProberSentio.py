"""
This file contains the implementation of the SentioProber class.
"""
import base64
import os
from typing import Tuple

from sentio_prober_control.Sentio.ProberBase import *
from sentio_prober_control.Sentio.CommandGroups.WafermapCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.VisionCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.StatusCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.SiPHCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.ServiceCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.ProbeCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.AuxCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.CompensationCommandGroup import *
from sentio_prober_control.Sentio.CommandGroups.QAlibriaCommandGroup import *
from sentio_prober_control.Sentio.Enumerations import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Communication.CommunicatorBase import *

class SentioProber(ProberBase):
    """ This class represents the SENTIO probe station in python. 
    
        It provides wrapper for most of the remote commands exposed by SENTIO and
    """
    def __init__(self, comm : CommunicatorBase):
        """ Construct a SENTIO prober object.
         
            The prober must be initialized with a communication object that specifies 
            how the system communicates with the probe station.

            :param comm: The communicator to use for communication with the prober.
        """
        ProberBase.__init__(self, comm)

        self.__name = "SentioProber"
        self.comm.send("*RCS 1")  # switch to the native SENTIO remote command set
        self.map : WafermapCommandGroup = WafermapCommandGroup(comm)
        """ The wafermap command group provides access to the wafermap modules functionality.  """

        self.aux : AuxCommandGroup = AuxCommandGroup(comm)
        """ The aux command group provides access the the aux site modules functionality. """

        self.vision : VisionCommandGroup = VisionCommandGroup(comm)
        """ The vision command group provides access to the vision modules functionality. """

        self.status : StatusCommandGroup = StatusCommandGroup(comm)
        """ The status command group provides access to the dashboard modules functionality. (formerly called status module)"""

        self.loader : LoaderCommandGroup = LoaderCommandGroup(comm)
        """ The loader command group provides access to the loader modules functionality. """

        self.siph : SiPHCommandGroup = SiPHCommandGroup(comm)
        """ The siph command group provides access to the SiPH modules functionality. """

        self.service : ServiceCommandGroup = ServiceCommandGroup(comm)
        """ The service command group provides access to the service modules functionality. """

        self.probe : ProbeCommandGroup = ProbeCommandGroup(comm)
        self.compensation : CompensationCommandGroup = CompensationCommandGroup(comm)
        self.qalibria : QAlibriaCommandGroup = QAlibriaCommandGroup(comm)


    def send_cmd(self, cmd: str) -> Response:
        """ Sends a command to the prober and return a response object.
        
            This function is intended for directly sending remote commands that
            are not yet included in the python wrapper. It will send the command 
            and parse the respone from SENTIO.

            It will then return a Response object with the extracted data from 
            SENTIO's response.

            :return: The response from the prober.
        """
        self.comm.send(cmd)
        return Response.check_resp(self.comm.read_line())


    def name(self):
        """ Returns the name of the prober. 
        
            :return: This function will always return the string "SentioProber".
        """
        return self.__name


    def connect(self):
        """ Establish a connection with the underlying communicator object. """
        self.__comm.connect()


    def query_command_status(self, cmd_id: int) -> Response:
        """ Query the status of an async command. 
        
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

            :param cmd_id: The id of the async command to query.
        """
        self.comm.send("query_command_status {0}".format(cmd_id))
        resp = Response.parse_resp(self.comm.read_line())
        return resp


    def open_project(self, project: str, restore_heights: bool = False):
        """ Open a SENTIO project file. 
        
            Wraps SENTIO's "open_project" remote command.

            :param project: The name or path of the project to open. If a full 
            path to the trex project file is given SENTIO will try to open this file. 
            If the argument does not contain a path SENTIO will look in its default
            project folder for a matching project and open it.
            :param restore_heights: If set to true SENTIO will restore the contact 
            heights from the project. Be carefull when using this option because
            the contact heights may have been become invalid since creating the project 
            due to a probe card change.
            :return: A response object with the result of the command.
            :raises: ProberException if an error occured.
        """
        self.comm.send(f"open_project {project}, {restore_heights}")
        Response.check_resp(self.comm.read_line())


    def save_project(self, project: str):
        """ Save the current SENTIO project. 
        
            Wraps SENTIO's "save_project" remote command.

            :return: A response object with the result of the command.
            :raises: ProberException if an error occured.
        """
        self.comm.send("save_project " + project)
        Response.check_resp(self.comm.read_line())


    def save_config(self):
        """ Save the SENTIO configuration file. 
            
            Wraps SENTIO's "save_config" remote command.

            :raises: ProberException if an error occured.
        """
        self.comm.send("save_config")
        Response.check_resp(self.comm.read_line())


    def move_chuck_separation(self) -> float:
        """ Move the chuck to separation height. 
            :raises: ProberException if an error occured.
            :return: The separation height in micrometer from chuck z axis zero.
        """
        self.comm.send("move_chuck_separation ")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_chuck_contact(self) -> float:
        """ Move the chuck to contact height. 

            Wraps SENTIO's "move_chuck_contact" remote command.

            :raises: ProberException if an error occured.
            :return: The contact height in micrometer from chuck z axis zero.
        """
        self.comm.send("move_chuck_contact")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_chuck_theta(self, ref:ChuckThetaReference, angle:float) -> float:
        """ Move chuck theta axis to a given angle. 

            Wraps SENTIO's "move_chuck_theta" remote command.

            :param ref: The reference to use for the move.
            :param angle: The angle to move to in degrees.
            :raises: ProberException if an error occured.
        """
        self.comm.send("move_chuck_theta {0}, {1}".format(ref.toSentioAbbr(), angle))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_chuck_xy(self, ref: ChuckXYReference, x:float, y:float) -> Tuple[float, float]:
        """ Move chuck to a given xy position. 

            Wraps SENTIO's "move_chuck_xy" remote command.

            :param ref: The reference to use for the move.
            :param x: The x position to move to in micrometer.
            :param y: The y position to move to in micrometer.
            :raises: ProberException if an error occured.
            :return: The actual x and y position in micrometer after the move.
        """
        self.comm.send("move_chuck_xy {0}, {1}, {2}".format(ref.toSentioAbbr(), x, y))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_chuck_z(self, ref: ChuckZReference, z:float) -> float:
        """ Move chuck to a given z position. 

            Wraps SENTIO's "move_chuck_z" remote command.

            :param ref: The z-reference to use for the move.
            :param z: The z position to move to in micrometer.
            :raises: ProberException if an error occured.
            :return: The actual z position in micrometer after the move.
        """
        self.comm.send("move_chuck_z {0}, {1}".format(ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_chuck_xy_pos(self) -> Tuple[float, float]:
        """ Returns the current xy position of the chuck. 

            Wraps SENTIO's "get_chuck_xy" remote command.

            :return: The actual x,y position in micrometer from axis zero.
        """
        self.comm.send('get_chuck_xy')
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        curX = float(tok[0])
        curY = float(tok[1])
        return curX, curY


    def get_chuck_theta(self, site: ChuckSite) -> float:
        """ Get the current angle of the chuck. 

            Wraps SENTIO's "get_chuck_theta" remote command.

            :param site: The chuck site to query.
            :raises: ProberException if an error occured.            
            :return: The current angle of the chuck site in degrees.
        """
        self.comm.send("get_chuck_theta {0}".format(site.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_chuck_site_status(self, site: ChuckSite) -> Tuple[bool, bool, bool, bool]:
        self.comm.send("get_chuck_site_status {0}".format(site.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")

        def str_to_bool(v: str):
            if (v=="0"):
                return False
            elif v=="1":
                return True
            else:
                return None

        hasHome = str_to_bool(tok[0])
        hasContact = str_to_bool(tok[1])
        overtravelActive = str_to_bool(tok[2])
        vacuumOn = str_to_bool(tok[3])

        return hasHome, hasContact, overtravelActive, vacuumOn


    def file_transfer(self, source: str, dest: str):
        # open file and encode with base64
        if not os.path.isfile(source):
            raise ProberException(f"File {source} not found!")

        file_bytes = open(source, "rb").read()
        encoded = base64.b64encode(file_bytes).decode('ascii')

        self.comm.send(f'file_transfer {dest}, {encoded}')
        Response.check_resp(self.comm.read_line())


    def get_chuck_site_height(self, site: ChuckSite) -> Tuple[float, float, float, float]:
        """
        Description: Retrieves height information of a chuck site\n
        Example: contact, separation, overtravel_gap, hover_gap = get_chuck_site_height(ChuckSite.Wafer)\n
        Gets for chuck site “Wafer” contact height, separation heights ,overtravel gap and hover height
        """
        self.comm.send("get_chuck_site_heights {0}".format(site.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")

        def str_to_bool(v: str):
            if (v=="0"):
                return False
            elif v=="1":
                return True
            else:
                return None

        contact = float(tok[0])
        separation = float(tok[1])
        overtravel_gap = float(tok[2])
        hover_gap = float(tok[3])

        return contact, separation, overtravel_gap, hover_gap


    def set_chuck_site_height(self, site: ChuckSite, contact: float, separation: float, overtravel_gap: float, hover_gap: float):
        """
        Description: Sets z position information of a chuck site\n
        Example: set_chuck_site_height(ChuckSite.Wafer,1000,800,20,5)\n
        Sets for chuck site “Wafer” contact height=1000 µm, separation heights=800 µm ,overtravel gap=20 µm and hover height=50 µm
        """
        par: str = "{},{},{},{},{}".format(site.toSentioAbbr(), contact, separation, overtravel_gap, hover_gap)
        self.comm.send("set_chuck_site_heights {0}".format(par))
        Response.check_resp(self.comm.read_line())


    def move_chuck_home(self) -> Tuple[float, float]:
        self.comm.send("move_chuck_home ")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    # Moves chuck to the last active position of the selected chuck site.
    def move_chuck_site(self, site:ChuckSite) -> Tuple[float, float, float, float]:
        self.comm.send("move_chuck_site {0}".format(site.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2]), float(tok[3])


    def move_chuck_load(self, pos: LoadPosition):
        self.comm.send("move_chuck_load {0}".format(pos.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()


    def move_chuck_work_area(self, site:WorkArea):
        self.comm.send("move_chuck_work_area {0}".format(site.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()


    def select_module(self, module: Module):
        self.comm.send(f"select_module {module.toSentioAbbr()}")
        Response.check_resp(self.comm.read_line())


    # Wait until all async commands have finished.
    # Added in SENTIO 3.6.2
    def wait_all(self, timeout: int = 90) -> Response:
        self.comm.send(f"wait_all {timeout}")
        return Response.check_resp(self.comm.read_line())


    def wait_complete(self, cmd_id: int, timeout: int = 90) -> Response:
        self.comm.send("wait_complete {0}, {1}".format(cmd_id, timeout))
        return Response.check_resp(self.comm.read_line())


    # Stop an ongoing remote command, no return value
    def abort_command(self, cmd_id: int) -> Response:
        self.comm.send("abort_command {0}".format(cmd_id))
        return Response.check_resp(self.comm.read_line())


    def start_initialization(self) -> Response:
        self.comm.send("start_initialization")
        return Response.check_resp(self.comm.read_line())


    # Initialize the prober if it is not already initialized
    def initialize_if_needed(self):
        isInitialized, isMeasuring, isLoaderBusy = self.status.get_machine_status()

        if (not isInitialized):
            resp = self.start_initialization()

            if (not resp.ok()):
                raise ProberException("Cannot start initialization: {0}".format(resp.message()))

            resp = self.wait_complete(resp.cmd_id(), 180)
            if (not resp.ok()):
                raise ProberException("Initialization failed: {0}".format(resp.message()))


    def has_chuck_xyz(self) -> bool:
        self.comm.send("has_chuck_xyz")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper()=="YES"


    def has_scope_xyz(self) -> bool:
        self.comm.send("has_scope_xyz")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper()=="YES"


    def has_scope_z(self) -> bool:
        self.comm.send("has_scope_z")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper()=="YES"


    def move_scope_xy(self, ref: ScopeXYReference, x:float, y:float) -> Tuple[float, float]:
        self.comm.send("move_scope_xy {0}, {1}, {2}".format(ref.toSentioAbbr(), x, y))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_scope_z(self, ref: ScopeZReference, z: float) -> float:
        self.comm.send("move_scope_z {0}, {1}".format(ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_scope_lift(self, state: bool) -> float:
        self.comm.send(f"move_scope_lift {state}")
        Response.check_resp(self.comm.read_line())


    def get_scope_xy(self) -> Tuple[float, float]:
        self.comm.send("get_scope_xy")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_scope_z(self) -> float:
        self.comm.send("get_scope_z")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_chuck_xy(self, site : ChuckSite, ref : ChuckXYReference) -> Tuple[float, float]:
        if (site is None):
            self.comm.send("get_chuck_xy {0}".format(site.toSentioAbbr()))
        else:
            self.comm.send("get_chuck_xy {0}, {1}".format(site.toSentioAbbr(), ref.toSentioAbbr()))

        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_chuck_z(self, ref : ChuckZReference) -> float:
        self.comm.send("get_chuck_z {0}".format(ref.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_vce_z(self, ref: VceZReference, z: float) -> float:
        self.comm.send("move_vce_z {0}, {1}".format(ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    #
    # Contact Handling
    #

    def clear_contact(self, site: ChuckSite = None):
        if site is None:
            self.comm.send("clear_contact")
        else:
            self.comm.send("clear_contact {0}".format(site.toSentioAbbr()))

        return Response.check_resp(self.comm.read_line())

    def set_stepping_contact_mode(self, mode: SteppingContactMode):
        self.comm.send("set_stepping_contact_mode {0}".format(mode.toSentioAbbr()))
        return Response.check_resp(self.comm.read_line())

    #
    # Asyn commands
    #

    def show_message(self, msg : str, buttons : DialogButtons,  caption : str, dialog_timeout : int = 180) -> DialogButtons:
        """ An command that will pop up a message box in SENTIO and wait for the result.

            Wraps SENTIO's "status:start_show_message" remote command.

            :param msg: The message to display.
            :param buttons: The buttons to display.
            :param caption: The caption of the message box.
            :param dialog_timeout: An optional dialog timeout in seconds after which the dialog will be closed automatically.
        """
        self.comm.send('status:start_show_message {0}, {1}, {2}'.format(msg, buttons.toSentioAbbr(), caption))
        resp = Response.check_resp(self.comm.read_line())

        # wait for button press
        self.comm.send('wait_complete {0}, {1}'.format(resp.cmd_id(), dialog_timeout))
        resp = Response.check_resp(self.comm.read_line())

        if (resp.message().lower()=="ok"):
            return DialogButtons.Ok

        if (resp.message().lower()=="cancel"):
            return DialogButtons.Cancel

        raise ProberException("Invalid dialog button return value")


    def show_hint_and_wait(self, msg : str, subtext: str, button_caption: str, timeout: int = 180, lock_ui: bool = True):
        """ Show an on screen message (hint) with a button wait for the button to be pressed. 

            Hints are on screen messages that pop up in SENTIO's lower left corner. This 
            overload will display a hint with a button and only return once the button has been pressed.

            This function wraps SENTIO's "status:show_hint" remote command.

            :param msg: The message to display.
            :param subtext: The subtext to display.
            :param button_caption: The caption of the button.
            :param timeout: An optional timeout in seconds after which the dialog will be closed automatically. (default = 180 s)
            :param lock_ui: An optional flag that determines wether the UI shall be locked. If this flag is set nothing but the button can be pressed.
            :raises: ProberException if an error occured.                        
            :return: None
        """
        self.comm.send('status:start_show_hint \"{0}\", \"{1}\", \"{2}\", \"{3}\"'.format(msg, subtext, button_caption, lock_ui))
        resp = Response.check_resp(self.comm.read_line())

        # wait for button press
        self.comm.send('wait_complete {0}, {1}'.format(resp.cmd_id(), timeout))
        Response.check_resp(self.comm.read_line())


    def show_hint(self, msg : str, subtext: str):
        """ Show an on screen message (hint) and return immediately 

            Hints are on screen messages that pop up in SENTIO's lower left corner. This hint will 
            disappears automatically after a few seconds.

            This function wraps SENTIO's "status:show_hint" remote command.

            :param msg: The message to display.
            :param subtext: The subtext to display.
            :raises: ProberException if an error occured.                        
            :return: None            
        """
        self.comm.send('status:show_hint \"{0}\", \"{1}\"'.format(msg, subtext))
        resp = Response.check_resp(self.comm.read_line())
        

    def get_project(self, pfi: ProjectFileInfo = ProjectFileInfo.FullPath) -> str:
        self.comm.send(f'get_project {pfi.toSentioAbbr()}')
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
