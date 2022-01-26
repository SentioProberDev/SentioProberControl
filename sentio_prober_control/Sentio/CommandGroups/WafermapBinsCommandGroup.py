from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *


class WafermapBinsCommandGroup(CommandGroupBase):
    def set_all(self, bin_val: int, selection: BinSelection):
        switcher = {
            BinSelection.All: "a",
            BinSelection.DiesOnly: "d",
            BinSelection.SubsitesOnly: "s"
        }

        what = switcher.get(selection, "Invalid bin selection")
        self._comm.send("map:bins:set_all {0}, {1}".format(bin_val, what))
        Response.check_resp(self._comm.read_line())#

    def load(self, file: str):
        self._comm.send("map:bins:load {0}".format(file))
        Response.check_resp(self._comm.read_line())

    def set_bin(self, bin_value: int, col: int, row: int, site=None):
        if site is None:
            self._comm.send("map:bins:set_bin {0}, {1}, {2}".format(bin_value, col, row))
        else:
            self._comm.send("map:bins:set_bin {0}, {1}, {2}, {3}".format(bin_value, col, row, site))
        Response.check_resp(self._comm.read_line())

    def clear_all(self):
        self._comm.send("map:bins:clear_all")
        Response.check_resp(self._comm.read_line())

    def clear_all_values(self):
        self._comm.send("map:bins:clear_all_values")
        Response.check_resp(self._comm.read_line())

    def set_value(self, value: float, col: int, row: int):
        self._comm.send("map:bins:set_value {0}, {1}, {2}".format(value, col, row))
        Response.check_resp(self._comm.read_line())