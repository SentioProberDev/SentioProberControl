from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *


class WafermapPathCommandGroup(CommandGroupBase):

    def select_dies(self, selection: TestSelection):
        switcher = {
            TestSelection.Nothing: "n",
            TestSelection.Good: "g",
            TestSelection.GoodAndUgly: "u",
            TestSelection.GoodUglyAndEdge: "e",
            TestSelection.All: "a"
        }

        what = switcher.get(selection, "Invalid die selection")
        self._comm.send("map:path:select_dies {0}".format(what))
        Response.check_resp(self._comm.read_line())

    def create_from_bin(self, bin_val: int):
        self._comm.send("map:path:create_from_bins {0}".format(bin_val))
        Response.check_resp(self._comm.read_line())

    def get_die(self, seq: int):
        self._comm.send("map:path:get_die {0}".format(seq))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return tok[0], tok[1]

    def set_routing(self, sp: RoutingStartPoint, pri: RoutingPriority):
        switcher1 = {
            RoutingStartPoint.UpperLeft: "ul",
            RoutingStartPoint.UpperRight: "ur",
            RoutingStartPoint.LowerLeft: "ll",
            RoutingStartPoint.LowerRight: "lr",
        }

        switcher2 = {
            RoutingPriority.RowUniDir: "r",
            RoutingPriority.ColUniDir: "c",
            RoutingPriority.RowBiDir: "wr",
            RoutingPriority.ColBiDir: "wc",
        }

        wsp = switcher1.get(sp, "Invalid route start point!")
        wpri = switcher2.get(pri, "Invalid routing priority!")

        self._comm.send("map:set_routing {0}, {1}".format(wsp, wpri))
        Response.check_resp(self._comm.read_line())