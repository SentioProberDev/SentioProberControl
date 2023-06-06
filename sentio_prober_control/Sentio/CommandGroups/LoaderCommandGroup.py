from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class LoaderCommandGroup(CommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm)

    def start_prepare_station(self, station: LoaderStation, angle: float = None) -> Response:
        if (angle==None):
            self._comm.send("loader:start_prepare_station {0}".format(station.toSentioAbbr()))
        else:
            self._comm.send("loader:start_prepare_station {0}, {1}".format(station.toSentioAbbr(), angle))

        return Response.check_resp(self._comm.read_line())

    def scan_station(self, station:LoaderStation) -> str:
        self._comm.send("loader:scan_station {0}".format(station.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def has_station(self, station:LoaderStation) -> bool:
        self._comm.send("loader:has_station {0}".format(station.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()=="1"

    def transfer_wafer(self, src_station:LoaderStation, src_slot:int, dst_station:LoaderStation, dst_slot:int):
        self._comm.send("loader:transfer_wafer {0}, {1}, {2}, {3}".format(src_station.toSentioAbbr(), src_slot,
                                                                           dst_station.toSentioAbbr(), dst_slot))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def load_wafer(self, src_station:LoaderStation, src_slot:int, angle: int):
        self._comm.send("loader:load_wafer {0}, {1}, {2}".format(src_station.toSentioAbbr(), src_slot, angle))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def prealign(self, marker: OrientationMarker, angle: int):
        self._comm.send("loader:prealign {0}, {1}".format(marker.toSentioAbbr(), angle))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def switch_work_area(self, area:str):
        self._comm.send("move_chuck_work_area {0}".format(area))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()

    def unload_wafer(self):
        self._comm.send("loader:unload_wafer")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()