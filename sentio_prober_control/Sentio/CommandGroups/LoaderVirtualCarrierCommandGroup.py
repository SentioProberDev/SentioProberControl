from typing import List

from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Response import Response


class LoaderVirtualCarrierCommandGroup(CommandGroupBase):
    """A command group for the Virtual Carrier functionality.

    You are not meant to instantiate this class directly. Access it via the loader attribute
    of the [SentioProber](SentioProber.md) class.
    """

    def __init__(self, comm) -> None:
        super().__init__(comm)


    def list(self) -> List[str]:
        """List all virtual carriers defined in SENTIO.

        Wraps Sentios "loader:vc:list" remote command.

        Returns:
            carriers (Tuple[str]): A tuple with the names of the virtual carriers.
        """

        try:
            self._comm.send("loader:vc:list")
            resp = Response.check_resp(self._comm.read_line())
            
            list : List[str] = resp.message().split(',')
            return list
        except:
            return []
        

    def select(self, vc_name : str) -> Response:
        """Select a virtual carrier.

        Wraps Sentios "loader:vc:select" remote command.

        Args:
            vc_name (str): The name of the virtual carrier to select.

        Returns:
            response (Response): A Response object.
        """

        self._comm.send(f"loader:vc:select {vc_name}")
        return Response.check_resp(self._comm.read_line())


    def start_load_first(self, cleanup : bool = False) -> Response:
        """Start loading the first wafer in the selected virtual carrier.
            
            This is an async command. You need to wait for the command to 
            complete.

        Wraps Sentios "loader:vc:start_load_first" remote command.

        Returns:
            resp (Response): A response object.
        """

        self._comm.send(f"loader:vc:start_load_first {cleanup}")
        resp = Response.check_resp(self._comm.read_line())
        return resp


    def load_first(self, cleanup : bool = False, timeout : int = 90) -> None:
        """Loads the first wafer of the virtual carrier. This is a blocking version of the start_load_first method.
            
            Wraps Sentios "loader:vc:start_load_first" remote command.

            Args:
                cleanup (bool): A boolean flag to indicate the wafer on the chuck shall be returned to its origin
                timeour (int): The timeout in seconds. (default is 90 seconds
        """

        resp : Response = self.start_load_first(cleanup)
        self._comm.send(f"wait_complete {resp.cmd_id()}, {timeout}")
        Response.check_resp(self._comm.read_line())


    def start_load_next(self) -> Response:
        """Start loading the next wafer in the selected virtual carrier.
            
            This is an async command. You need to wait for the command to 
            complete.

            Wraps Sentios "loader:vc:start_load_next" remote command.

        Returns:
            resp (Response): A response object.
        """

        self._comm.send(f"loader:vc:start_load_next")
        resp = Response.check_resp(self._comm.read_line())
        return resp
    
    
    def load_next(self, timeout : int = 90) -> None:
        """Loads the first wafer of the virtual carrier. This is a blocking version of the start_load_first method.
            
            Wraps Sentios "loader:vc:start_load_first" remote command.

            Args:
                cleanup (bool): A boolean flag to indicate the wafer on the chuck shall be returned to its origin
                timeour (int): The timeout in seconds. (default is 90 seconds
        """

        resp : Response = self.start_load_next()
        self._comm.send(f"wait_complete {resp.cmd_id()}, {timeout}")
        Response.check_resp(self._comm.read_line())
