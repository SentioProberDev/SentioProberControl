from deprecated import deprecated
from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import LoaderStation, OrientationMarker, RemoteCommandError
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


    def start_prepare_station(self, station: LoaderStation, angle: float | None = None) -> Response:
        """Prepare a loader station for wafer processing.

        This command will trigger a scan of all wafers in a station. This command is an async
        remote command!

        Wraps Sentios "loader:start_prepare_station" remote command.

        Args:
            station (LoaderStation): The station to prepare.
            angle (float): The prealignment angle. If None, no prealignment will be done.

        Returns:
            response (Response): A Response object.
        """

        if angle == None:
            self.comm.send(f"loader:start_prepare_station {station.toSentioAbbr()}")
        else:
            self.comm.send(f"loader:start_prepare_station {station.toSentioAbbr()}, {angle}")

        return Response.check_resp(self.comm.read_line())


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


    def transfer_wafer(
        self,
        src_station: LoaderStation,
        src_slot: int,
        dst_station: LoaderStation,
        dst_slot: int
    ):
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
        return Response.check_resp(self.comm.read_line())


    def load_wafer(self, src_station: LoaderStation, src_slot: int, angle: int | None = None):
        """Load a wafer onto the chuck with optional prealignment.

        Args:
            src_station: The source station.
            src_slot: The source slot.
            angle: The prealignment angle.

        Returns:
            response (Response): A Response object.
        """

        if angle is None:
            self.comm.send(f"loader:load_wafer {src_station.toSentioAbbr()}, {src_slot}")
        else:
            self.comm.send(f"loader:load_wafer {src_station.toSentioAbbr()}, {src_slot}, {angle}")

        return Response.check_resp(self.comm.read_line())


    def prealign(self, marker: OrientationMarker, angle: int):
        """Prealign a wafer.

        Wraps Sentios "loader:prealign" remote command.

        Args:
            marker (OrientationMarker): The type of wafer orientation marker.
            angle (float): The prealignment angle.

        Returns:
            response (Response): A Response object.
        """

        self.comm.send(f"loader:prealign {marker.toSentioAbbr()}, {angle}")
        return Response.check_resp(self.comm.read_line())

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
    

    @deprecated("duplicate functionality; Use SentioProber.move_chuck_work_area!")
    def switch_work_area(self, area: str):
        self.comm.send("move_chuck_work_area {0}".format(area))
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()


    def unload_wafer(self) -> None:
        """Unload the current wafer from the chuck.

        Wraps Sentios "loader:unload_wafer" remote command.
        """

        self.comm.send("loader:unload_wafer")
        Response.check_resp(self.comm.read_line())
