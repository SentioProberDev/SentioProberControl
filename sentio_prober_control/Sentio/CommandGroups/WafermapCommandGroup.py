from typing import Tuple
from deprecated import deprecated

from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.ProberBase import ProberException
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.CommandGroups.WafermapBinsCommandGroup import  WafermapBinsCommandGroup
from sentio_prober_control.Sentio.CommandGroups.WafermapPathCommandGroup import  WafermapPathCommandGroup
from sentio_prober_control.Sentio.CommandGroups.WafermapPoiCommandGroup import  WafermapPoiCommandGroup
from sentio_prober_control.Sentio.CommandGroups.WafermapSubsiteCommandGroup import  WafermapSubsiteGroup
from sentio_prober_control.Sentio.CommandGroups.WafermapCompensationCommandGroup import  WafermapCompensationCommandGroup
from sentio_prober_control.Sentio.CommandGroups.WafermapDieCommandGroup import  WafermapDieCommandGroup
from sentio_prober_control.Sentio.Enumerations import *


class WafermapCommandGroup(ModuleCommandGroupBase):
    """ This class represents the SENTIO command group for wafermap related commands."""

    def __init__(self, comm):
        """ Creates the wafermap command group. 
        
            The wafermap command group contains several other command groups that handle
            aspects of the wafermap and stepping.
        """
        super().__init__(comm, 'map')
        self.__end_of_route: bool = False

        self.subsites : WafermapSubsiteGroup = WafermapSubsiteGroup(comm, self)
        """ A group the handle subsites. """

        self.path : WafermapPathCommandGroup = WafermapPathCommandGroup(comm)
        """ A group the handle setting up tests paths. """

        self.bins : WafermapBinsCommandGroup = WafermapBinsCommandGroup(comm)
        """ A group to set up the binning."""

        self.die : WafermapDieCommandGroup = WafermapDieCommandGroup(comm)
        """ A group to set up the die."""

        self.poi : WafermapPoiCommandGroup = WafermapPoiCommandGroup(comm)
        """ A group for working with points of interest."""

        self.compensation : WafermapCompensationCommandGroup = WafermapCompensationCommandGroup(comm)
        """ A command group with functions for setting up and executing x,y and z compensation."""


    def create(self, diameter: float):
        """ Create a new round wafer map. 
        
            Wraps Sentios "map:create" remote command.

            :param diameter: The diameter of the wafer.
            :raises: ProberException if an error occured.            
        """
        self._comm.send(f"map:create {diameter}")
        Response.check_resp(self._comm.read_line())


    def create_rect(self, cols: int, rows: int):
        """ Create a new rectangular wafer map.

            Wraps Sentios "map:create_rect" remote command.

            :param cols: The number of columns.
            :param rows: The number of rows.
            :raises: ProberException if an error occured.
        """
        self._comm.send("map:create_rect {0}, {1}".format(cols, rows))
        Response.check_resp(self._comm.read_line())


    def get_axis_orient(self) -> AxisOrient:
        """ Get axis orientation of the wafer map. 
        
            Wraps Sentios "map:get_axis_orient" remote command.

            :raises: ProberException if an error occured.
            :return: The axis orientation.
        """

        self._comm.send("map:get_axis_orient")
        resp = Response.check_resp(self._comm.read_line())

        if resp.message().upper()=="UL":
            return AxisOrient.UpLeft

        if resp.message().upper()=="UR":
            return AxisOrient.UpRight

        if resp.message().upper()=="DR":
            return AxisOrient.DownRight

        if resp.message().upper()=="DL":
            return AxisOrient.DownLeft


    def get_diameter(self) -> float:
        """ Get diameter of the wafer map im millimeter. 
            
            Wraps Sentios "map:get_diameter" remote command.
        
            :raises: ProberException if an error occured.
            :returns: The diameter of the wafer map in millimeter.
        """
        self._comm.send("map:get_diameter")
        resp = Response.check_resp(self._comm.read_line())

        dia = int(resp.message())
        return dia


    def get_grid_origin(self) -> Tuple[int, int]:
        """ Get origin of the wafermap grid. 

            Wraps Sentios "map:get_grid_origin" remote command.

            :raises: ProberException if an error occured.
            :returns: A tuple with the column and row indices of the origin. 
         """
        self._comm.send("map:get_grid_origin")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")

        return int(tok[0]), int(tok[1])


    def get_index_size(self) -> Tuple[float, float]:
        """ Return the die size set up in the wafer map.
         
            :raises: ProberException if an error occured.
            :returns: A tuple with the die width and height in micrometer.
         """
        self._comm.send("map:get_index_size")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_street_size(self) -> Tuple[int, int]:
        """ Returns the street size set up in the wafer map.
         
            In SENTIO the street size is merely a visual aid. It is not used for 
            any calculations. The only purpose is rendering the diese in a more
            realistic manner.

            :raises: ProberException if an error occured.
            :return: A tuple with the street width and height in micrometer.
        """
        self._comm.send("map:get_street_size")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")

        return int(tok[0]), int(tok[1])


    def get_num_dies(self, selection: DieNumber) -> int:
        """ Returns the number of dies in the wafer map. 
        
            :param selection: The selection of dies to count.
            :raises: ProberException if an error occured.
            :return: The number of dies.
        """
        switcher = {
            DieNumber.Present: "Present",
            DieNumber.Selected: "Selected"
        }

        what = switcher.get(selection, "Invalid die number selector")

        self._comm.send("map:get_num_dies {0}".format(what))
        resp = Response.check_resp(self._comm.read_line())
        return int(resp.message())


    def get_die_seq(self) -> int:
        """ Returns the sequence number of the current die. 
        
            The sequence number id the index of the die in the 
            current stepping sequence. The stepping sequence 
            contains the dies selected for test. 
            The sequence number is zero based and is also displayed 
            in the wafermap when zoomin into a die.

            Wraps Sentios "map:get_die_seq" remote command.

            :raises: ProberException if an error occured.
            :return: The sequence number of the current die.
        """
        self._comm.send("map:get_die_seq")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()  # 0:Result+status, 1:Command ID, 2:Response


    def set_flat_params(self, angle: float, width: float):
        self._comm.send("map:set_flat_params {0}, {1}".format(angle, width))
        Response.check_resp(self._comm.read_line())


    def set_index_size(self, x: float, y: float):
        self._comm.send("map:set_index_size {0}, {1}".format(x, y))
        Response.check_resp(self._comm.read_line())


    def set_grid_params(self, ix: float, iy: float, offx: float, offy: float, edge: float):
        self._comm.send("map:set_grid_params {0}, {1}, {2}, {3}, {4}".format(ix, iy, offx, offy, edge))
        Response.check_resp(self._comm.read_line())


    def set_grid_origin(self, x: int, y: int):
        self._comm.send("map:set_grid_origin {0}, {1}".format(x, y))
        Response.check_resp(self._comm.read_line())


    def set_home_die(self, x: int, y: int):
        self._comm.send("map:set_home_die {0}, {1}".format(x, y))
        Response.check_resp(self._comm.read_line())


    def set_street_size(self, x: float, y: float):
        self._comm.send("map:set_street_size {0}, {1}".format(x, y))
        Response.check_resp(self._comm.read_line())

    def die_reference_is_set(self) -> bool:
        self._comm.send("map:get_prop die_reference_is_set")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message().lower()=='true'

    def get_die_reference(self) -> Tuple[float, float]:
        self._comm.send("map:get_prop die_reference")
        resp = Response.check_resp(self._comm.read_line())

        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def set_axis_orient(self, orient: AxisOrient):
        switcher = {
            AxisOrient.UpRight: "ur",
            AxisOrient.DownLeft: "dl",
            AxisOrient.DownRight: "dr",
            AxisOrient.UpLeft: "ul"
        }

        what = switcher.get(orient, "Invalid axis orientation")
        self._comm.send("map:set_axis_orient {0}".format(what))
        Response.check_resp(self._comm.read_line())

    def set_color_scheme(self, scheme: ColorScheme):
        self._comm.send(f'map:set_color_scheme {scheme.toSentioAbbr()}')
        Response.check_resp(self._comm.read_line())

    ###############################################################################################
    #
    # Stepping
    #
    ###############################################################################################

    def step_first_die(self, site: int=None) -> Tuple[int, int, int]:
        if site == None:
            self._comm.send("map:step_first_die")
        else:
            self._comm.send(f"map:step_first_die {site}")
            
        resp = Response.parse_resp(self._comm.read_line())
        
        self.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute
        
        if not resp.ok():
            raise ProberException(resp.message(), resp.errc())
            
        tok = resp.message().split(",")

        return int(tok[0]), int(tok[1]), int(tok[2])

    def step_die(self, col:int, row:int, site: int = 0) -> Tuple[int, int, int]:
        self._comm.send("map:step_die {0}, {1}, {2}".format(col, row, site))
        resp = Response.parse_resp(self._comm.read_line())

        self.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute

        if not resp.ok():
            raise ProberException(resp.message(), resp.errc())

        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])

    def step_next_die(self) -> Tuple[int, int, int]:
        self._comm.send("map:step_next_die")
        resp = Response.parse_resp(self._comm.read_line())

        self.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute

        if not resp.ok():
            raise ProberException(resp.message(), resp.errc())

        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])

    def bin_step_next_die(self, bin_value: int, site: int = None) -> Tuple[int, int, int]:
        # 2021-09-17: bugfix: when no site is given current site must be retained
        if site is None:
            self._comm.send(f'map:bin_step_next_die {bin_value}')
        else:
            self._comm.send(f'map:bin_step_next_die {bin_value}, {site}')

        resp = Response.parse_resp(self._comm.read_line())
        self.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute

        # i.e. Stepping while at the end of the route
        if not resp.ok():
            raise ProberException(resp.message(), resp.errc())

        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])

    def step_next_die(self, site: int = None) -> Tuple[int, int, int]:
        # 2021-09-17: bugfix: when no site is given current site must be retained
        if site is None:
            self._comm.send(f'map:step_next_die')
        else:
            self._comm.send(f'map:step_next_die {site}')

        resp = Response.parse_resp(self._comm.read_line())
        self.__end_of_route = (resp.status() & StatusBits.EndOfRoute) == StatusBits.EndOfRoute

        # i.e. Stepping while at the end of the route
        if not resp.ok():
            raise ProberException(resp.message(), resp.errc())

        tok = resp.message().split(",")
        return int(tok[0]), int(tok[1]), int(tok[2])

    def step_die_seq(self, seq: int, site: int) -> Tuple[int, int, int]:
        self._comm.send("map:step_die_seq {}, {}".format(seq, site))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")

        # i.e. Stepping while at the end of the route
        if not resp.ok():
            raise ProberException(resp.message())

        return int(tok[0]), int(tok[1]), int(tok[2])

    def end_of_route(self):
        return self.__end_of_route
