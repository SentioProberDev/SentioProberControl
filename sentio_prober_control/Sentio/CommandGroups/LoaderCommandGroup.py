from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class LoaderCommandGroup(CommandGroupBase):
    """ This command group contains functions for working with the loader. """

    def __init__(self, comm):
        """ @private """
        super().__init__(comm)


    def start_prepare_station(self, station: LoaderStation, angle: float = None) -> Response:
        """ Prepare a loader station for wafer processing.  
        
            This command will trigger a scan of all wafers in a station. This command is an async 
            remote command!
        
            Wraps Sentios "loader:start_prepare_station" remote command.

            :param station: The station to prepare.
            :param angle: The prealignment angle. If None, no prealignment will be done.
            :rasies: ProberException if an error occured.
            :returns: A Response object.
        """
        if (angle==None):
            self._comm.send(f"loader:start_prepare_station {station.toSentioAbbr()}")
        else:
            self._comm.send(f"loader:start_prepare_station {station.toSentioAbbr()}, {angle}")

        return Response.check_resp(self._comm.read_line())


    def scan_station(self, station:LoaderStation) -> str:
        """ Scans a loader station for wafers. 
            Wraps Sentios "loader:scan_station" remote command.

            :param station: The station to scan.
            :raises: ProberException if an error occured.
            :return: A string with the scan result.
        """
        self._comm.send(f"loader:scan_station {station.toSentioAbbr()}")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()


    def has_station(self, station:LoaderStation) -> bool:
        """ Check wether a certain loader station is present.
         
            Wraps Sentios "loader:has_station" remote command.
             
            :param station: The station to check.
            :raises: ProberException if an error occured.
            :returns: True if the station is present, False otherwise.
        """
        self._comm.send(f"loader:has_station {station.toSentioAbbr()}")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()=="1"


    def transfer_wafer(self, src_station:LoaderStation, src_slot:int, dst_station:LoaderStation, dst_slot:int):
        """ Transfer a wafer from one loader station to another. 
            :param src_station: The source station.
            :param src_slot: The source slot.
            :param dst_station: The destination station.
            :param dst_slot: The destination slot.
        """
        self._comm.send(f"loader:transfer_wafer {src_station.toSentioAbbr()}, {src_slot}, {dst_station.toSentioAbbr()}, {dst_slot}")
        return Response.check_resp(self._comm.read_line())


    def load_wafer(self, src_station:LoaderStation, src_slot:int, angle: int):
        """ Load a wafer onto the chuck with optional prealignment. 

            :param src_station: The source station.
            :param src_slot: The source slot.
            :param angle: The prealignment angle.
            :raises: ProberException if an error occured.
            :returns: A Response object.
        """
        self._comm.send(f"loader:load_wafer {src_station.toSentioAbbr()}, {src_slot}, {angle}")
        return Response.check_resp(self._comm.read_line())


    def prealign(self, marker: OrientationMarker, angle: int):
        """ Prealign a wafer. 
         
            Wraps Sentios "loader:prealign" remote command.

            :param marker: The type of wafer orientation marker.
            :param angle: The prealignment angle.
            :returns: A Response object.
        """
        self._comm.send(f"loader:prealign {marker.toSentioAbbr()}, {angle}")
        return Response.check_resp(self._comm.read_line())


    @deprecated("duplicate functionality; Use SentioProber.move_chuck_work_area!")
    def switch_work_area(self, area:str):
        """ Move chuck to a different work area.

            This function is deprecated. Do not use it in new code and remove all 
            occurrences in existing code. The function will be removed in a future 
            version! 

            Use the SentioProber.move_chuck_work_area function instead!
         """
        self._comm.send("move_chuck_work_area {0}".format(area))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()


    def unload_wafer(self):
        """ Unload the current wafer from the chuck.

            Wraps Sentios "loader:unload_wafer" remote command.

            :raises: ProberException if an error occured.
            :returns: A Response object.         
        """
        self._comm.send("loader:unload_wafer")
        return Response.check_resp(self._comm.read_line())
