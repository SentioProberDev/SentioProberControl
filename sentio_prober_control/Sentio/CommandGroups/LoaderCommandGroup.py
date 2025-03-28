from deprecated import deprecated
from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import LoaderStation, OrientationMarker, RemoteCommandError, WaferStatusItem
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.CommandGroups.LoaderVirtualCarrierCommandGroup import LoaderVirtualCarrierCommandGroup
from sentio_prober_control.Communication.CommunicatorBase import CommunicatorBase
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

        self.vc: LoaderVirtualCarrierCommandGroup = LoaderVirtualCarrierCommandGroup(self)


    def has_station(self, station: LoaderStation) -> bool:
        """Check wether a certain loader station is present.

        Wraps Sentios "loader:has_station" remote command.

        Args:
            station (LoaderStation): The station to check.

        Returns:
            has_station (bool): True if the station is present, False otherwise.
        """

        self.comm.send(f"loader:has_station {station.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message() == "1"
    

    def load_wafer(self, src_station: LoaderStation, src_slot: int, angle: int | None = None) -> None:
        """Load a wafer onto the chuck with optional prealignment.

        Args:
            src_station: The source station.
            src_slot: The source slot.
            angle: The prealignment angle.
        """

        if angle is None:
            self.comm.send(f"loader:load_wafer {src_station.toSentioAbbr()}, {src_slot}")
        else:
            self.comm.send(f"loader:load_wafer {src_station.toSentioAbbr()}, {src_slot}, {angle}")

        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def prealign(self, marker: OrientationMarker, angle: int) -> None:
        """Prealign a wafer.

        Wraps Sentios "loader:prealign" remote command.

        Args:
            marker (OrientationMarker): The type of wafer orientation marker.
            angle (float): The prealignment angle.
        """

        self.comm.send(f"loader:prealign {marker.toSentioAbbr()}, {angle}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def query_wafer_status(self, station : LoaderStation, slot : int) -> Tuple[LoaderStation, int, int, int, float] | None:
        """Query the status of a wafer in a loader station.

        Wraps Sentios "loader:query_wafer_status" remote command.

        Args:
            station (LoaderStation): The station to query.
            slot (int): The slot to query.

        Returns:
            status (Tuple[LoaderStation, int, int, int, float]): A tuple with the following elements: OriginStation, OriginSlot, Wafer Size, Wafer Orientation, Progress Value.
        """

        self.comm.send(f"loader:query_wafer_status {station.toSentioAbbr()}, {slot}")
        
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

        self.comm.send(f"loader:scan_station {station.toSentioAbbr()}")
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
        self.comm.send(f"loader:set_wafer_status {station.toSentioAbbr()},{slot},{what.toSentioAbbr()},{value}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def start_prepare_station(self, station: LoaderStation, angle: float | None = None) -> None:
        """Prepare a loader station for wafer processing.

        This command will trigger a scan of all wafers in a station. This command is an async
        remote command!

        Wraps Sentios "loader:start_prepare_station" remote command.

        Args:
            station (LoaderStation): The station to prepare.
            angle (float): The prealignment angle. If None, no prealignment will be done.
        """

        if angle == None:
            self.comm.send(f"loader:start_prepare_station {station.toSentioAbbr()}")
        else:
            self.comm.send(f"loader:start_prepare_station {station.toSentioAbbr()}, {angle}")

        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

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

        self.comm.send(
            f"loader:transfer_wafer {src_station.toSentioAbbr()}, {src_slot}, {dst_station.toSentioAbbr()}, {dst_slot}"
        )
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()


    def unload_wafer(self) -> None:
        """Unload the current wafer from the chuck.

        Wraps Sentios "loader:unload_wafer" remote command.
        """

        self.comm.send("loader:unload_wafer")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()

    def has_cassette(self,station : LoaderStation) -> None:
        
        """Query whether a cassette is present in a given cassette station.

        Args:
            station (LoaderStation): The cassette station to scan

        """
        
        self.comm.send(f"loader:has_cassette {station.toSentioAbbr()}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def set_wafer_id(self,station : LoaderStation, slot : int, waferid : str) -> None:
        
        """Reset the wafer id.

        Args:
            station (LoaderStation): The  station to reset waferid
            slot(int):The slot to reset waferid

        """
        
        self.comm.send(f"loader:set_wafer_id {station.toSentioAbbr}, {slot}, {waferid}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def query_wafer_id(self,station : LoaderStation, slot : int) -> None:
        
        """Query the wafer id that already existing.

        Args:
            station (LoaderStation): The  station to query waferid
            slot(int):The slot to query waferid
        """
        
        self.comm.send(f"loader:query_wafer_id {station.toSentioAbbr}, {slot}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def read_wafer_id(self,angle : str, side : str) -> None:
        
        """Command will trigger ID Reader to read wafer id.

        Args:
            angle(str):Wafer ID angle
            side(str):Wafer ID side
        """
        
        self.comm.send(f"loader:read_wafer_id {angle}, {side}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def start_prepare_wafer(self,station : LoaderStation, slot : int, angle : int, readid : int, unloadstation : LoaderStation, unloadslot : int) -> None:
        
        """Set the wafer to default state

        """
        
        self.comm.send(f"loader:start_prepare_wafer {station.toSentioAbbr}, {slot}, {angle}, {readid}, {unloadstation}, {unloadslot}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def swap_wafer(self) ->None:
        
        """
            For dual-fork loader: Wafer form chuck is placed on loader fork A, wafer from loader fork A is placed on chuck.
            For single-fork loader: Wafer form chuck is placed on its origin station, wafer from pre-aligner is placed on chuck.

        """
        
        self.comm.send(f"loader:swap_wafer")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def query_station_status(self, station : LoaderStation) ->None:
        
        """Returns the wafer presence state of a station without losing wafer information.

        Args:
            station(LoaderStation):query station status.
        
        """
        
        self.comm.send(f"loader:query_station_status {station.toSentioAbbr}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def start_read_wafer_id(self, angle : str, side : str) ->None:
        
        """Command will trigger ID Reader to read wafer id._summary_

        """
        
        self.comm.send(f"loader:start_read_wafer_id {angle}, {side}")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()