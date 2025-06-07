from deprecated import deprecated
from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import LoaderStation, OrientationMarker, RemoteCommandError, WaferStatusItem, WaferIdSide
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.CommandGroups.LoaderVirtualCarrierCommandGroup import LoaderVirtualCarrierCommandGroup
from sentio_prober_control.Sentio.ProberBase import ProberException


class LoaderCommandGroup(CommandGroupBase):

    """This command group contains functions for working with the loader.
    You are not meant to instantiate this class directly. Access it via the loader attribute
    of the [SentioProber](SentioProber.md) class.

    Example:

    ```py
    from sentio_prober_control.Sentio.ProberSentio import SentioProber

    prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
    scan_result = prober.loader.scan_station(LoaderStation.Cassette1)
    ```
    """

    def __init__(self, parent : 'SentioProber') -> None:
        super().__init__(parent)

        self.vc : LoaderVirtualCarrierCommandGroup = LoaderVirtualCarrierCommandGroup(self)


    def has_station(self, station: LoaderStation) -> bool:

        """Check wether a certain loader station is present.

        Wraps Sentios "loader:has_station" remote command.

        Args:
            station (LoaderStation): The station to check.

        Returns:
            has_station (bool): True if the station is present, False otherwise.
        """

        self.comm.send(f"loader:has_station {station.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message() == "1"
    

    def load_wafer(self, src_station: LoaderStation, src_slot: int, angle: int | None = None) -> str:

        """Load a wafer onto the chuck with optional prealignment.

        Args:
            src_station: The source station.
            src_slot: The source slot.
            angle: The prealignment angle.

        Returns:
            If the system has an id reader the wafer id of the loaded wafer is returned. 
        """

        if angle is None:
            self.comm.send(f"loader:load_wafer {src_station.to_string()}, {src_slot}")
        else:
            self.comm.send(f"loader:load_wafer {src_station.to_string()}, {src_slot}, {angle}")

        resp = Response.check_resp(self.comm.read_line())
        if resp.message().lower() == "ok":
            # SENTIO would return "ok" if the system does not have an id reader. make sure to never return "ok" as an id.
            return ""
        else:
            return resp.message()


    def prealign(self, marker: OrientationMarker, angle: int) -> None:

        """Prealign a wafer.

        Wraps Sentios "loader:prealign" remote command.

        Args:
            marker (OrientationMarker): The type of wafer orientation marker.
            angle (float): The prealignment angle.
        """

        self.comm.send(f"loader:prealign {marker.to_string()}, {angle}")
        Response.check_resp(self.comm.read_line())

    def query_wafer_status(self, station : LoaderStation, slot : int) -> Tuple[LoaderStation, int, int, int, float] | None:

        """Query the status of a wafer in a loader station.

        Wraps Sentios "loader:query_wafer_status" remote command.

        Args:
            station (LoaderStation): The station to query.
            slot (int): The slot to query.

        Returns:
            status (Tuple[LoaderStation, int, int, int, float]): A tuple with the following elements: OriginStation, OriginSlot, Wafer Size, Wafer Orientation, Progress Value.
        """

        self.comm.send(f"loader:query_wafer_status {station.to_string()}, {slot}")
        
        try:
            resp = Response.check_resp(self.comm.read_line())
        except ProberException as e: 
            if e.error() == RemoteCommandError.SlotOrStationEmpty:
                return None
            else:
                raise
        
        tok = resp.message().split(',')
        origin_station = LoaderStation[tok[0]]
        origin_slot = int(tok[1])
        
        try:
           # SENTIO may return NaN for unknown size
           size = int(tok[2])
        except:
            size = -1

        orient = int(tok[3])
        progress = float(tok[4])

        return (origin_station, origin_slot, size, orient, progress)


    def scan_station(self, station: LoaderStation) -> str:

        """Scans a loader station for wafers.
        Wraps Sentios "loader:scan_station" remote command.

        Args:
            station (LoaderStation): The station to scan.

        Returns:
            result (str): A string with the scan result.
        """

        self.comm.send(f"loader:scan_station {station.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    

    def set_wafer_status(self, station: LoaderStation, slot : int, what : WaferStatusItem, value : float) -> None:

        """ Set status of a wafer in the wafer tracker.
        Wraps Sentios "loader:set_wafer_status" remote command.

        Args:
            station (LoaderStation): The station of the wafer.
            slot (int): The slot in which the wafer is located. The index is 1-based.
            what (WaferStatusItem): Defines which status iten shall be set.
            value (float): The value to set.
        """
        
        self.comm.send(f"loader:set_wafer_status {station.to_string()},{slot},{what.to_string()},{value}")
        Response.check_resp(self.comm.read_line())
        

    def start_prepare_station(self, station: LoaderStation, angle: float | None = None) -> Response:
        """Prepare a loader station for wafer processing.

        This command will trigger a scan of all wafers in a station. This command is an async
        remote command!

        Wraps Sentios "loader:start_prepare_station" remote command.

        Args:
            station (LoaderStation): The station to prepare.
            angle (float): The prealignment angle. If None, no prealignment will be done.

        Returns:
            Response: A response object with the async command id. You need to use wait_complete or wait_all to wait 
            for the command to finish.
        """

        if angle == None:
            self.comm.send(f"loader:start_prepare_station {station.to_string()}")
        else:
            self.comm.send(f"loader:start_prepare_station {station.to_string()}, {angle}")

        return Response.check_resp(self.comm.read_line())

    @deprecated("duplicate functionality; Use SentioProber.move_chuck_work_area!")
    def switch_work_area(self, area: str):
        self.comm.send("move_chuck_work_area {0}".format(area))
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def transfer_wafer(
        self,
        src_station: LoaderStation,
        src_slot: int,
        dst_station: LoaderStation,
        dst_slot: int) -> None:
        """Transfer a wafer from one loader station to another.

        Args:
            src_station (LoaderStation): The source station.
            src_slot (int): The source slot.
            dst_station (LoaderStation): The destination station.
            dst_slot (int): The destination slot.
        """

        self.comm.send(f"loader:transfer_wafer {src_station.to_string()}, {src_slot}, {dst_station.to_string()}, {dst_slot}")
        Response.check_resp(self.comm.read_line())


    def unload_wafer(self, station : LoaderStation | None = None, slot : int = 1) -> None:
        """ System will execute unloading wafer from chuck to wafer wallet max (TS3500/TS2000IFE), 
        wafer wallet (TS3500) or Cassette (TS2500), or Side Door (TS2000-SE). Wafer wallet max works with cassette, so the parameter station is cassette1.

            Wraps Sentios "loader:unload_wafer" remote command.

        Args:
            dest_station (LoaderStation): The destination station.
            dest_slot (int): The destination slot.
        """

        if station is not None:
            self.comm.send(f"loader:unload_wafer {station.to_string()}, {slot}")
        else:
            self.comm.send("loader:unload_wafer")

        Response.check_resp(self.comm.read_line())
        

    def has_cassette(self,station : LoaderStation) -> Tuple[bool, int]:
        
        """Query whether a cassette is present in a given cassette station.

        Args:
            station (LoaderStation): The cassette station to scan

        Returns:
            has_cassette (bool): True if a cassette is present, False otherwise.
            cassette_size (int): The size of the cassette in mm. 0 if no cassette is present.
        """
        
        self.comm.send(f"loader:has_cassette {station.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(',')
        has_cassette = tok[0] == "1"
        cassette_size = int(tok[1])
        return has_cassette, cassette_size

    
    def set_wafer_id(self,station : LoaderStation, slot : int, waferid : str) -> str:
        
        """Reset the wafer id.

        Args:
            station (LoaderStation): The  station to reset waferid
            slot(int):The slot to reset waferid

        """
        
        self.comm.send(f"loader:set_wafer_id {station.to_string()}, {slot}, {waferid}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def query_wafer_id(self,station : LoaderStation, slot : int) -> str:
        
        """Query the wafer id that already existing.

        Args:
            station (LoaderStation): The  station to query waferid
            slot(int):The slot to query waferid
        """
        
        self.comm.send(f"loader:query_wafer_id {station.to_string()}, {slot}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    

    def read_wafer_id(self, angle : int | None = None, side : WaferIdSide | None = None) -> str:
        
        """ Command will trigger ID Reader to read wafer id.

        Args:
            angle(int|None): Rotate wafer to this angle. Do nothing if angle is None.
            side(WaferIdSide): Side of the wafer on which the id is located.

        Returns:
            wafer_id (str): The wafer id read by the ID reader.
        """
        
        if angle is None and side is None:
            self.comm.send(f"loader:read_wafer_id")
        elif angle is not None and side is not None:
            self.comm.send(f"loader:read_wafer_id {angle}, {side.to_string()}")
        else:
            raise ValueError("Both angle or side must be given or neither of those.")
            
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    

    def start_prepare_wafer(self, station : LoaderStation, slot : int, angle : int, read_id : bool, unloadstation : LoaderStation, unloadslot : int) -> Response:
        
        """ Set the wafer to default state.

            This is an async command! You need to use wait_complete or wait_all to wait for the command to finish.

        Args:
            station (LoaderStation): Source station of the wafer.
            slot (int): Source slot of the wafer.
            angle (int): The prealignment angle.
            readid (bool): If True, the ID reader will be triggered to read the wafer id.
            unloadstation (LoaderStation): The station to unload the wafer to.
            unloadslot (int): The slot to unload the wafer to.

        Returns:
            Response: A response object with the async command id. You need to use wait_complete or wait_all to wait
            for the command to finish.
        """
        
        self.comm.send(f"loader:start_prepare_wafer {station.to_string()}, {slot}, {angle}, {1 if read_id else 0}, {unloadstation.to_string()}, {unloadslot}")
        return Response.check_resp(self.comm.read_line())


    def swap_wafer(self) -> Tuple[bool, bool]:
        
        """ Swap Wafers.
        
        For dual-fork loader: Wafer form chuck is placed on loader fork A, wafer from loader fork A is placed on chuck.
        For single-fork loader: Wafer form chuck is placed on its origin station, wafer from pre-aligner is placed on chuck.

        Returns:
                bool: True if the wafer was unloaded from the chuck successfully.
                bool: True if the wafer was loaded onto the chuck successfully.
        """
        
        self.comm.send(f"loader:swap_wafer")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(',')
        return bool(tok[0]), bool(tok[1])
    

    def query_station_status(self, station : LoaderStation) -> str:
        
        """Returns the wafer presence state of a station without losing wafer information.

        Args:
            station(LoaderStation):query station status.
        
        Returns:
            status (str): A string consisting of "0" and "1" indicating the presence of a wafer in a slot of the station.
        """
        
        self.comm.send(f"loader:query_station_status {station.to_string()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    

    def start_read_wafer_id(self, angle : int, side : WaferIdSide) -> Response:
        
        """ Command will trigger ID Reader to read wafer id. A wafer must be on the PreAligner. 
            If id reading failes, SENTIO will show a message box to display the failed id image to 
            user to input correct id.

        Args:
            angle (int): Rotate wafer to this angle.
            side (WaferIdSide): Side of the wafer on which the id is located.

        Returns:
            Response: A response object with the async command id. You need to use wait_complete or wait_all to wait
            for the command to finish.
        """
        
        self.comm.send(f"loader:start_read_wafer_id {angle}, {side.to_string()}")
        return Response.check_resp(self.comm.read_line())
