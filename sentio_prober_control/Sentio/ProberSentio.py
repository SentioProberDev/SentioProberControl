""" This package contains the implementation of the SentioProber class.

    # Overview

    The SentioProber class is your gateway to control a probe station running the MPI SENTIO 
    Software suite.

    Some functionality is provided directy via member functions of the class.
    The following example triggers a switch of the active SENTIO module by using the 
    select_module function:

    >>> from sentio_prober_control.Sentio.ProberSentio import *
    >>> from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
    >>> prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))
    >>> prober.select_module(Module.Wafermap)


    Most functionality is grouped into so called command groups that are accessible 
    through the member variables listed below. A command group is merely a class that groups a number 
    of prober related functions together. The available command groups are:
    * aux (sentio_prober_control.Sentio.CommandGroups.AuxCommandGroup.AuxCommandGroup)
    * loader (sentio_prober_control.Sentio.CommandGroups.LoaderCommandGroup.LoaderCommandGroup)
    * map (sentio_prober_control.Sentio.CommandGroups.WafermapCommandGroup.WafermapCommandGroup)
    * probe
    * qalibria
    * service
    * siph
    * status
    * vis

    To access a function associated with a command group simply add the name of the command group to
    the prober call. The following example would call the switch_all_lights command from the 
    vision command group:

    >>> prober.vis.switch_all_lights(False)
"""
import base64
import os
from typing import Tuple
from deprecated import deprecated

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
from sentio_prober_control.Communication.CommunicatorGpib import *
from sentio_prober_control.Communication.CommunicatorTcpIp import *
from sentio_prober_control.Communication.CommunicatorVisa import *


class SentioProber(ProberBase):
    """ This class represents the SENTIO probe station in python. 
        It provides wrapper for most of the remote commands exposed by SENTIO.
    """

    def __init__(self, comm : CommunicatorBase):
        """ Construct a SENTIO prober object.
         
            The prober must be initialized with a communication object that 
            specifies how the system communicates with the probe station.

            :param comm: The communicator to use for communication with the prober.
        """
        ProberBase.__init__(self, comm)

        self.__name = "SentioProber"
        self.comm.send("*RCS 1")  # switch to the native SENTIO remote command set

        self.aux : AuxCommandGroup = AuxCommandGroup(comm)
        """ The aux command group provides access the the aux site modules functionality. 
        
            Example:
            >>> from sentio_prober_control.Sentio.ProberSentio import *
            >>> from sentio_prober_control.Communication.CommunicatorTcpIp import CommunicatorTcpIp
            >>> prober = SentioProber(CommunicatorTcpIp.create("127.0.0.1:35555"))
            >>> prober.aux.cleaning.enable_auto(True)
        """

        self.compensation : CompensationCommandGroup = CompensationCommandGroup(comm)
        """ Command group for accessing functionalitly for x,y and z-compensation. 

            This command group is deprecated! Use prober.vis.compensation instead.

            @private    
        """

        self.loader : LoaderCommandGroup = LoaderCommandGroup(comm)
        """ The loader command group provides access to the loader modules functionality. """

        self.map : WafermapCommandGroup = WafermapCommandGroup(comm)
        """ The wafermap command group provides access to the wafermap modules functionality.  """

        self.probe : ProbeCommandGroup = ProbeCommandGroup(comm)
        """ Command group for accessing functionalitly for motorized probes. """

        self.qalibria : QAlibriaCommandGroup = QAlibriaCommandGroup(comm)
        """ Command group for accessing the QAlibria modules functionality. """

        self.service : ServiceCommandGroup = ServiceCommandGroup(comm)
        """ The service command group provides access to the service modules functionality. """

        self.siph : SiPHCommandGroup = SiPHCommandGroup(comm)
        """ The siph command group provides access to the SiPH modules functionality. """

        self.status : StatusCommandGroup = StatusCommandGroup(comm)
        """ The status command group provides access to the dashboard modules functionality. (formerly called status module)"""

        self.vision : VisionCommandGroup = VisionCommandGroup(comm)
        """ The vision command group provides access to the vision modules functionality. """


    def abort_command(self, cmd_id: int) -> Response:
        """ Stop an ongoing asynchronous remote command.

            :param cmd_id: The id of the async command to abort. 
            :raises: ProberException if an error occured.            
            :return: A response object with the result of the command.             
        """
        self.comm.send("abort_command {0}".format(cmd_id))
        return Response.check_resp(self.comm.read_line())


    def clear_contact(self, site: ChuckSite = None):
        """ Clear contact positions.

            :param  site: The chuck site to clear. If None is given all sites will be cleared.
            :raises: ProberException if an error occured.
            :return: None
        """
        if site is None:
            self.comm.send("clear_contact")
        else:
            self.comm.send(f"clear_contact {site.toSentioAbbr()}")

        return Response.check_resp(self.comm.read_line())
    
    @staticmethod
    def create_prober(comm_type : str ="tcpip", arg1 = "127.0.0.1:35556", arg2 = None) -> 'SentioProber':
        """ Create an instance of a SentioProber object with a certain type of communication.
         
            .. versionadded:: 23.2

            :param comm_type: The type of communication to use. Valid values are "tcpip", "gpib" and "visa".
            :param kwargs: The arguments to pass to the communicator constructor. For tcpip this is a single string specifying address and port like "127.0.0.1:35556". 
            For gpib these are two parameters. The first one for specifying the type of card (NI/ADLINK), the second one being the gpib address string. 
         """
        
        if comm_type == "tcpip":
            return SentioProber(CommunicatorTcpIp.create(arg1))
        elif comm_type == "gpib":
            return SentioProber(CommunicatorGpib.create(arg1, arg2))
        elif comm_type == "visa":        
            return SentioProber(CommunicatorVisa.create(arg1))
        else:
            raise ValueError("Unknown prober type")


    def file_transfer(self, source: str, dest: str):
        """ Transfer a file to the prober. 
        
            This function will transfer a file to the prober. The file will be stored in the position specified by dast.
            The file will be transmitted in base64 encoding which can take some time.
            
            :param source: The path to the file to transfer.
            :param dest: The destination path on the prober. Must be a complete path including file name. Make sure that SENTIO has write access to the given destination.
            :raises: ProberException if an error occured.            
            :return: None
        """
        # open file and encode with base64
        if not os.path.isfile(source):
            raise ProberException(f"File {source} not found!")

        file_bytes = open(source, "rb").read()
        encoded = base64.b64encode(file_bytes).decode('ascii')

        self.comm.send(f'file_transfer {dest}, {encoded}')
        Response.check_resp(self.comm.read_line())


    def get_chuck_site_height(self, site: ChuckSite) -> Tuple[float, float, float, float]:
        """ Retrieves height information of a chuck site
        
            Example: 
        
            >>> contact, separation, overtravel_dist, hover_gap = get_chuck_site_height(ChuckSite.Wafer)
        
            Gets for chuck site "Wafer" contact height, separation heights ,overtravel distance and hover height

            :param site: The chuck site to query.
            :raises: ProberException if an error occured.            
            :return: A tuple with the contact height, separation height, overtravel distance and hover height in micrometer.
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


    def get_chuck_site_status(self, site: ChuckSite) -> Tuple[bool, bool, bool, bool]:
        """ Get status of a chuck site. 
         
            Wraps SENTIO's "get_chuck_site_status" remote command.

            :param site: The chuck site to query.
            :raises: ProberException if an error occured.
            :return: A tuple with the status of the chuck site. The tuple contains the following values:
            * hasHome: True if the chuck site has a home position.
            * hasContact: True if the chuck site has a contact position.
            * overtravelActive: True if the overtravel is active.
            * vacuumOn: True if the vacuum is on.    
        """
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


    def get_chuck_xy(self, site : ChuckSite, ref : ChuckXYReference) -> Tuple[float, float]:
        """ Get current chuck xy position with respect to a given reference.

            :param site: The chuck site to query.
            :param ref: The reference to use for the query.
            :raises: ProberException if an error occured.
            :return: The actual x,y position in micrometer.
        """

        if (site is None):
            self.comm.send(f"get_chuck_xy {site.toSentioAbbr()}")
        else:
            self.comm.send(f"get_chuck_xy {site.toSentioAbbr()}, {ref.toSentioAbbr()}")

        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    @deprecated(reason="Duplicate functionality; Use get_chuck_xy instead")
    def get_chuck_xy_pos(self) -> Tuple[float, float]:
        """ Returns the current xy position of the chuck. 

            .. deprecated:: 23.2

            Use get_chuck_xy instead.

            :return: The actual x,y position in micrometer from axis zero.
           
        """

        self.comm.send('get_chuck_xy')
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        curX = float(tok[0])
        curY = float(tok[1])
        return curX, curY


    def get_chuck_z(self, ref : ChuckZReference) -> float:
        """ Get chuck z position. 
        
            :param ref: The reference to use for the query.
            :raises: ProberException if an error occured.
            :return: The actual z position of the chuck in micrometer (from axis zero).
        """

        self.comm.send("get_chuck_z {0}".format(ref.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def get_project(self, pfi: ProjectFileInfo = ProjectFileInfo.FullPath) -> str:
        """ Get the name of the current project. 
            
            :raises: A ProberException is raised if no project is loaded.
            :return The name of the current project.
        """
        self.comm.send(f'get_project {pfi.toSentioAbbr()}')
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()


    def get_scope_xy(self) -> Tuple[float, float]:
        """ Get current scope xy position. 

            The returned position is an absolute position with respect to the axis zero in micrometer.

            :raises: ProberException if an error occured.                               
            :return: The actual x,y position in micrometer.
        """
        self.comm.send("get_scope_xy")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_scope_z(self) -> float:
        """ Get scope z position in micrometer from axis zero.
            
            :raises: ProberException if an error occured.
            :return: The actual z position in micrometer. 
        """
        self.comm.send("get_scope_z")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())
    

    def has_chuck_xyz(self) -> bool:
        """ Returns True if the chuck has xyz axes.
            :raises: ProberException if an error occured.       
            :return: True if the chuck has xyz axes.
        """
        self.comm.send("has_chuck_xyz")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper()=="YES"


    def has_scope_xyz(self) -> bool:
        """ Returns True if the scope has xyz axes.
            :raises: ProberException if an error occured.       
            :return: True if the scope has xyz axes.
        """
        self.comm.send("has_scope_xyz")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper()=="YES"


    def has_scope_z(self) -> bool:
        """ Returns true if the microscope has a motorized z axis.
            :raises: ProberException if an error occured.       
            :return: True if the scope has xyz axes.
        """
        self.comm.send("has_scope_z")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message().upper()=="YES"
    

    def initialize_if_needed(self):
        """ Initialize the prober if it is not already initialized. 

            This command will check if the prober is already initialized. If not
            it will start the initialization process and wait for it to complete.

            You do not have to call waitcomplete after this function on your own!

            :raises: ProberException if an error occured.       
            :return: None
        """
        isInitialized, isMeasuring, isLoaderBusy = self.status.get_machine_status()

        if (not isInitialized):
            resp = self.start_initialization()

            if (not resp.ok()):
                raise ProberException("Cannot start initialization: {0}".format(resp.message()))

            resp = self.wait_complete(resp.cmd_id(), 180)
            if (not resp.ok()):
                raise ProberException("Initialization failed: {0}".format(resp.message()))


    def local_mode(self):
        """ Switch the prober back into local mode.

            .. versionadded:: 23.2

            The probe station will automatically enter remote mode when a remote command is received. 
            It will remian in remote mode even after the script is finished. This command can be used 
            to switch the machine back into local mode and thus enable its UI.
        """
        self.comm.send("*LOCAL")


    def move_chuck_contact(self) -> float:
        """ Move the chuck to contact height. 

            Wraps SENTIO's "move_chuck_contact" remote command.

            :raises: ProberException if an error occured.
            :return: The contact height in micrometer from chuck z axis zero.
        """
        self.comm.send("move_chuck_contact")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())
    

    def move_chuck_home(self) -> Tuple[float, float]:
        """ Move chuck to its home position.
            :raises: ProberException if an error occured.
            :return: The actual x,y position in micrometer (with respect to axis zero).   
        """
        self.comm.send("move_chuck_home ")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])
    

    def move_chuck_load(self, pos: LoadPosition):
        """ Move chuck to load position.
         
            Wraps SENTIO's "move_chuck_load" remote command.

            :param  pos: The load position to move to.    
            :raises: ProberException if an error occured.
            :Return: A response object with the result of the command.
        """
        self.comm.send("move_chuck_load {0}".format(pos.toSentioAbbr()))
        return Response.check_resp(self.comm.read_line())
        

    def move_chuck_separation(self) -> float:
        """ Move the chuck to separation height. 
            :raises: ProberException if an error occured.
            :return: The separation height in micrometer from chuck z axis zero.
        """
        self.comm.send("move_chuck_separation ")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_chuck_site(self, site:ChuckSite) -> Tuple[float, float, float, float]:
        """ Moves chuck to the last active position of the selected chuck site.

            Wraps SENTIO's "move_chuck_site" remote command.

            :raises: ProberException if an error occured.
            :return: A tuple consisting of 4 floating point values representing the chuck position after the move. The tuple contains the following values:
            * x: The x position in micrometer.
            * y: The y position in micrometer.
            * z: The z height in micrometer.
            * theta: The theta angle in degrees.
        """
        self.comm.send("move_chuck_site {0}".format(site.toSentioAbbr()))
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2]), float(tok[3])
    

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


    def move_chuck_work_area(self, site:WorkArea):
        """ Move the chuck to a given work area.
         
            Wraps SENTIO's "move_chuck_work_area" remote command.   

            :param site: The work area to move to.
            :raises: ProberException if an error occured.
            :return: A response object with the result of the command.
        """
        self.comm.send("move_chuck_work_area {0}".format(site.toSentioAbbr()))
        return Response.check_resp(self.comm.read_line())
    

    def move_scope_xy(self, ref: ScopeXYReference, x:float, y:float) -> Tuple[float, float]:
        """ Move scope to a given xy position. 

            :param ref: The reference to use for the move.
            :param x: The x position to move to in micrometer.
            :param y: The y position to move to in micrometer.
            :raises: ProberException if an error occured.                   
            :return The actual x,y position in micrometer after the move.
        """
        self.comm.send("move_scope_xy {0}, {1}, {2}".format(ref.toSentioAbbr(), x, y))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_scope_lift(self, state: bool) -> float:
        """ Move scope to its lift position.
         
            The scope lift position is a position where the scope is
            at its axis maximum. This position will give you the maximum
            possible are of unhindered operation when changing probe cards
            or other maintenance tasks.

            :param state: True to move to the lift position, False to move away from the lift position.  
            :return: None
         """
        self.comm.send(f"move_scope_lift {state}")
        Response.check_resp(self.comm.read_line())


    def move_scope_z(self, ref: ScopeZReference, z: float) -> float:
        """ Move scope to a given z position. 
            :param ref: The reference to use for the move.
            :param z: The z position to move to in micrometer.
            :raises: ProberException if an error occured.                               
            :return: The actual z position in micrometer after the move.
        """
        self.comm.send("move_scope_z {0}, {1}".format(ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def move_vce_z(self, stage:Stage, ref: VceZReference, z: float) -> float:
        """ Move VCE stage to a given z position.
         
            :param ref: The reference to use for the move.
            :param z: The z position to move to in micrometer.
            :raises: ProberException if an error occured.
            :return: The actual z position in micrometer after the move.
        """
        if stage != Stage.Vce and stage != Stage.Vce2:
            raise ProberException(f"This command can only be applied to vce stages! (stage={0})")
        
        self.comm.send(f"move_vce_z {stage.toSentioAbbr()}, {ref.toSentioAbbr()}, {z}")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())


    def name(self):
        """ Returns the name of the prober. 
        
            :return: This function will always return the string "SentioProber".
        """
        return self.__name


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
    

    def save_config(self):
        """ Save the SENTIO configuration file. 
            
            Wraps SENTIO's "save_config" remote command.

            :raises: ProberException if an error occured.
        """
        self.comm.send("save_config")
        Response.check_resp(self.comm.read_line())


    def save_project(self, project: str):
        """ Save the current SENTIO project. 
        
            Wraps SENTIO's "save_project" remote command.

            :return: A response object with the result of the command.
            :raises: ProberException if an error occured.
        """
        self.comm.send("save_project " + project)
        Response.check_resp(self.comm.read_line())


    def select_module(self, module: Module):
        """ Activate a given SENTIO module. 
        
            In response to this function SENTIO will switch its user interface to make 
            the given module the active one.

            This function wraps the "select_module" remote command of SENTIO.

            :param module: The module to activate.
            :raises: ProberException if an error occured.
            :return: A response object with the result of the command.
        """
        self.comm.send(f"select_module {module.toSentioAbbr()}")
        return Response.check_resp(self.comm.read_line())
    

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
    

    def set_chuck_site_height(self, site: ChuckSite, contact: float, separation: float, overtravel_dist: float, hover_gap: float):
        """ Sets z position information of a chuck site
        
            Example:
            
            >>> set_chuck_site_height(ChuckSite.Wafer,16000,250,20,50)

            Will set the contact height of the wafer site to 16000 µm with a separation height of 250 µm an overtravel of 20 and a hover height of 50

            :param site: The chuck site to query.
            :param contact: The new contact height in micrometer.
            :param separation: The new separation height in micrometer.
            :param overtravel_dist: The new overtravel distance in micrometer.
            :param hover_gap: The new hover gap in micrometer.
            :raises: ProberException if an error occured.
            :return: None
        """
        par: str = "{},{},{},{},{}".format(site.toSentioAbbr(), contact, separation, overtravel_dist, hover_gap)
        self.comm.send("set_chuck_site_heights {0}".format(par))
        Response.check_resp(self.comm.read_line())


    def set_stepping_contact_mode(self, mode: SteppingContactMode):
        """ Change the stepping contact mode.
         
            The stepping contact mode defines what happens during stepping over a wafer.
            The following modes are available:
            * BackToContact: The chuck will step into contact position
            * StepToSeparation: The chuck will step into separation position. You have to move into contact with a seaparate command.
            * LockContack: The Chuck is not allowed to leave contact position automatically as part of a stepping command. You have to move into separation with a separate command bevore being able to step to the next die..

            :param mode: The stepping contact mode to set.
            :raises: ProberException if an error occured.
            :return: A response object with the result of the command.
         """
        self.comm.send("set_stepping_contact_mode {0}".format(mode.toSentioAbbr()))
        return Response.check_resp(self.comm.read_line())


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
        self.comm.send(f'status:show_hint \"{msg}\", \"{subtext}\"')
        resp = Response.check_resp(self.comm.read_line())


    def show_hint_and_wait(self, msg : str, subtext: str, button_caption: str, timeout: int = 180, lock_ui: bool = True):
        """ Show an on screen message with a button wait for a button to be pressed. 

            Hints pop up in SENTIO's lower left corner. This function will display a hint with a button 
            and only return once the button has been pressed.

            :param msg: The message to display.
            :param subtext: The subtext to display. Subtext is displayed in a second line with a slightly smaller font.
            :param button_caption: The caption of the button.
            :param timeout: An optional timeout in seconds after which the dialog will be closed automatically. (default = 180 s)
            :param lock_ui: An optional flag that determines wether the UI shall be locked. Most of the UI is disabled in 
            remote mode anyway. This button affects only the on screen interactions on the right side of the main module view. (default = True)
            :raises: ProberException if an error occured.                        
            :return: None
        """
        self.comm.send(f'status:start_show_hint \"{msg}\", \"{subtext}\", \"{button_caption}\", \"{lock_ui}\"')
        resp = Response.check_resp(self.comm.read_line())

        # wait for button press
        self.comm.send(f'wait_complete {resp.cmd_id()}, {timeout}')
        Response.check_resp(self.comm.read_line())


    def show_message(self, msg : str, buttons : DialogButtons,  caption : str, dialog_timeout : int = 180) -> DialogButtons:
        """ Pop up a message dialog in SENTIO and wait for the result.

            :param msg: The message to display.
            :param buttons: The buttons to display.
            :param caption: The caption of the message box.
            :param dialog_timeout: An optional dialog timeout in seconds after which the dialog will be closed automatically.
            :raises: ProberException if an error occured.
            :return: The button that was as an DialogButtons enum value.
        """
        self.comm.send('status:start_show_message {0}, {1}, {2}'.format(msg, buttons.toSentioAbbr(), caption))
        resp = Response.check_resp(self.comm.read_line())

        # wait for button press
        self.comm.send('wait_complete {0}, {1}'.format(resp.cmd_id(), dialog_timeout))
        resp = Response.check_resp(self.comm.read_line())

        if (resp.message().lower()=="ok"):
            return DialogButtons.Ok

        if (resp.message().lower()=="yes"):
            return DialogButtons.Yes

        if (resp.message().lower()=="no"):
            return DialogButtons.No

        if (resp.message().lower()=="cancel"):
            return DialogButtons.Cancel

        raise ProberException("Invalid dialog button return value")
    
    
    def start_initialization(self) -> Response:
        """ Start the initialization of the probe station. 
        
            This function will start the initialization of the prober. This is an 
            async command that will return immediately.

            The initialization process will take some time to complete. Use
            waitcomplete to wait for the initialization to complete.

            :raises: ProberException if an error occured.
            :return: A response object with the result of the command.
        """
        self.comm.send("start_initialization")
        return Response.check_resp(self.comm.read_line())


    def wait_all(self, timeout: int = 90) -> Response:
        """ Wait until all async commands have finished.

            added in SENTIO 3.6.2        

            :param timeout: The timeout in seconds.
            :raises: ProberException if an error occured.            
            :return: A response object with the result of the command.
        """
        self.comm.send(f"wait_all {timeout}")
        return Response.check_resp(self.comm.read_line())


    def wait_complete(self, cmd_id: int, timeout: int = 90) -> Response:
        """ Wait for a single async command to complete.
            :param cmd_id: The id of the async command to wait for.
            :param timeout: The timeout in seconds.
            :raises: ProberException if an error occured.            
            :return: A response object with the result of the command. 
        """
        self.comm.send("wait_complete {0}, {1}".format(cmd_id, timeout))
        return Response.check_resp(self.comm.read_line())



