from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class LoaderCommandGroup(CommandGroupBase):
    """ This command group contains functions for working with the loader. 
        You are not meant to create instances of this class on your own.
        Instead use the loader property of the SentioProber class.

        Example:
            
        ```py
            from sentio_prober_control.Sentio.ProberSentio import *

            prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
            scan_result = prober.loader.scan_station(LoaderStation.Cassette1)
        ```    
    """

    def __init__(self, comm):
        super().__init__(comm)


    def start_prepare_station(self, station: LoaderStation, angle: float = None) -> Response:
        """ Prepare a loader station for wafer processing.  
        
            This command will trigger a scan of all wafers in a station. This command is an async 
            remote command!
        
            Wraps Sentios "loader:start_prepare_station" remote command.

            Args:
                station (LoaderStation): The station to prepare.
                angle (float): The prealignment angle. If None, no prealignment will be done.
            
            Returns:
                response (Response): A Response object.
        """

        if (angle==None):
            self._comm.send(f"loader:start_prepare_station {station.toSentioAbbr()}")
        else:
            self._comm.send(f"loader:start_prepare_station {station.toSentioAbbr()}, {angle}")

        return Response.check_resp(self._comm.read_line())


    def scan_station(self, station:LoaderStation) -> str:
        """ Scans a loader station for wafers. 
            Wraps Sentios "loader:scan_station" remote command.

            Args:
                station (LoaderStation): The station to scan.
            
            Returns:
                result (str): A string with the scan result.
        """

        self._comm.send(f"loader:scan_station {station.toSentioAbbr()}")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()


    def has_station(self, station:LoaderStation) -> bool:
        """ Check wether a certain loader station is present.
         
            Wraps Sentios "loader:has_station" remote command.
             
            Args:
                station (LoaderStation): The station to check.
            
            Returns:
                has_station (bool): True if the station is present, False otherwise.
        """

        self._comm.send(f"loader:has_station {station.toSentioAbbr()}")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()=="1"


    def transfer_wafer(self, src_station:LoaderStation, src_slot:int, dst_station:LoaderStation, dst_slot:int):
        """ Transfer a wafer from one loader station to another. 

            Args:
                src_station (LoaderStation): The source station.
                src_slot (int): The source slot.
                dst_station (LoaderStation): The destination station.
                dst_slot (int): The destination slot.
        """

        self._comm.send(f"loader:transfer_wafer {src_station.toSentioAbbr()}, {src_slot}, {dst_station.toSentioAbbr()}, {dst_slot}")
        return Response.check_resp(self._comm.read_line())


    def load_wafer(self, src_station:LoaderStation, src_slot:int, angle: int):
        """ Load a wafer onto the chuck with optional prealignment. 

            Args:
                src_station: The source station.
                src_slot: The source slot.
                angle: The prealignment angle.

            Returns:
                response (Response): A Response object.
        """

        self._comm.send(f"loader:load_wafer {src_station.toSentioAbbr()}, {src_slot}, {angle}")
        return Response.check_resp(self._comm.read_line())


    def prealign(self, marker: OrientationMarker, angle: int):
        """ Prealign a wafer. 
         
            Wraps Sentios "loader:prealign" remote command.

            Args:
                marker (OrientationMarker): The type of wafer orientation marker.
                angle (float): The prealignment angle.

            Returns:
                response (Response): A Response object.
        """

        self._comm.send(f"loader:prealign {marker.toSentioAbbr()}, {angle}")
        return Response.check_resp(self._comm.read_line())


    @deprecated("duplicate functionality; Use SentioProber.move_chuck_work_area!")
    def switch_work_area(self, area:str):
        self._comm.send("move_chuck_work_area {0}".format(area))
        resp = Response.check_resp(self._comm.read_line())
        return resp.message()


    def unload_wafer(self):
        """ Unload the current wafer from the chuck.

            Wraps Sentios "loader:unload_wafer" remote command.

            Returns:
                response (Response): A Response object.
        """

        self._comm.send("loader:unload_wafer")
        return Response.check_resp(self._comm.read_line())
