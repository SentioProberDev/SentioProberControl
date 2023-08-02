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

class SentioProber(ProberBase):
    def __init__(self, comm):
        ProberBase.__init__(self, comm)

        self.__name = "SentioProber"
        self.comm.send("*RCS 1")  # switch to the native SENTIO remote command set
        self.map = WafermapCommandGroup(comm)
        self.aux = AuxCommandGroup(comm)
        self.vision = VisionCommandGroup(comm)
        self.status = StatusCommandGroup(comm)
        self.loader = LoaderCommandGroup(comm)
        self.siph = SiPHCommandGroup(comm)
        self.service = ServiceCommandGroup(comm)
        self.probe = ProbeCommandGroup(comm)
        self.compensation = CompensationCommandGroup(comm)
        self.qalibria = QAlibriaCommandGroup(comm)

    def send_cmd(self, cmd: str):
        self.comm.send(cmd)
        return Response.check_resp(self.comm.read_line())

    def name(self):
        return self.__name

    def connect(self):
        self.__comm.connect()

    def query_command_status(self, cmd_id: int) -> Tuple[Response, int]:
        self.comm.send("query_command_status {0}".format(cmd_id))
        resp = Response.parse_resp(self.comm.read_line())
        return resp

    def open_project(self, project: str, restore_heights: bool = False):
        self.comm.send(f"open_project {project}, {restore_heights}")
        Response.check_resp(self.comm.read_line())

    def save_project(self, project: str):
        self.comm.send("save_project " + project)
        Response.check_resp(self.comm.read_line())

    def save_config(self):
        self.comm.send("save_config")
        Response.check_resp(self.comm.read_line())

    def move_chuck_separation(self) -> float:
        self.comm.send("move_chuck_separation ")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_chuck_contact(self) -> float:
        self.comm.send("move_chuck_contact")
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_chuck_theta(self, ref:ChuckThetaReference, angle:float) -> float:
        self.comm.send("move_chuck_theta {0}, {1}".format(ref.toSentioAbbr(), angle))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def move_chuck_xy(self, ref: ChuckXYReference, x:float, y:float) -> Tuple[float, float]:
        self.comm.send("move_chuck_xy {0}, {1}, {2}".format(ref.toSentioAbbr(), x, y))
        resp = Response.check_resp(self.comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def move_chuck_z(self, ref: ChuckZReference, z:float) -> float:
        self.comm.send("move_chuck_z {0}, {1}".format(ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.comm.read_line())
        return float(resp.message())

    def get_chuck_xy_pos(self):
        self.comm.send('get_chuck_xy')
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        curX = float(tok[0])
        curY = float(tok[1])
        return curX, curY

    def get_chuck_theta(self, site: ChuckSite) -> float:
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

    """ show_hint_and_wait with button, wait for button press before returning """
    def show_hint_and_wait(self, msg : str, subtext: str, button_caption: str, timeout: int = 180, isLockGui: bool = True):
        self.comm.send('status:start_show_hint \"{0}\", \"{1}\", \"{2}\", \"{3}\"'.format(msg, subtext, button_caption, isLockGui))
        resp = Response.check_resp(self.comm.read_line())

        # wait for button press
        self.comm.send('wait_complete {0}, {1}'.format(resp.cmd_id(), timeout))
        Response.check_resp(self.comm.read_line())

    """ show_hint return immediately """
    def show_hint(self, msg : str, subtext: str):
        self.comm.send('status:show_hint \"{0}\", \"{1}\"'.format(msg, subtext))
        resp = Response.check_resp(self.comm.read_line())

    def get_project(self, pfi: ProjectFileInfo = ProjectFileInfo.FullPath) -> str:
        self.comm.send(f'get_project {pfi.toSentioAbbr()}')
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
