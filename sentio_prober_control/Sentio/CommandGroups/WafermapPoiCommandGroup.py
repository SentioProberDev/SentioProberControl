from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *


class WafermapPoiCommandGroup(CommandGroupBase):
    """ A command group for working with Points of Interest (POI) on the wafermap. """

    def add(self, x, y, desc) -> None:
        """ Add a POI to the list. 

            Wraps SENTIO's map:poi:add remote command.

            :param x: The x coordinate of the POI.
            :param y: The y coordinate of the POI.
            :param desc: The description of the POI.
            :raises ProberException: if the command could not be executed successfully.     
        """
        self._comm.send("map:poi:add {0}, {1}, {2}".format(x, y, desc))
        Response.check_resp(self._comm.read_line())


    def get_num(self) -> int:
        """ Returns the number of POIs in the list.

            Wraps SENTIO's map:poi:get_num remote command.

            :raises ProberException: if the command could not be executed successfully.
            :return: The number of POIs in the list.
        """
        self._comm.send("map:poi:get_num")
        resp = Response.check_resp(self._comm.read_line())
        return int(resp.message())


    def reset(self, stage : Stage, refXy : PoiReferenceXy) -> None:
        """ Reset the list of POIs.

            Clears the list and resets its stage and position reference settings.
            
            Wraps SENTIO's map:poi:reset remote command.

            :param stage: The stage to reset the POIs for.
            :param refXy: The reference point for the POIs. 
            :raises ProberException: if the command could not be executed successfully.
        """
        self._comm.send("map:poi:reset {0}, {1}".format(stage.toSentioAbbr(), refXy.toSentioAbbr()))
        Response.check_resp(self._comm.read_line())


    def step(self, target) -> None:
        """ Step to a POI in the list. 

            Wraps SENTIO's map:poi:step remote command.

            :param target: The target POI to step to.
            :raises ProberException: if the command could not be executed successfully.
        """
        self._comm.send("map:poi:step {0}".format(target))
        Response.check_resp(self._comm.read_line())


    def step_first(self) -> None:
        """ Step to the first POI in the list.
         
            Wraps SENTIO's map:poi:step_first remote command.

            :raises ProberException: if the command could not be executed successfully.
         """
        self._comm.send("map:poi:step_first")
        Response.check_resp(self._comm.read_line())


    def step_next(self) -> None:
        """ Step to the next POI in the list.

            Wrap SENTIO's map:poi:step_next remote command.

            :raises ProberException: if the command could not be executed successfully.
        """
        self._comm.send("map:poi:step_next")
        Response.check_resp(self._comm.read_line())

