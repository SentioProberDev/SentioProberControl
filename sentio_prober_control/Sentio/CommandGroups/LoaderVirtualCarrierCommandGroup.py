import re

from typing import List, Tuple

from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.Helper import Helper
from sentio_prober_control.Sentio.Enumerations import VirtualCarrierInitFlags, VirtualCarrierStepProcessingState, LoaderStation


class LoaderVirtualCarrierCommandGroup(CommandGroupBase):
    """A command group for the Virtual Carrier functionality.

    You are not meant to instantiate this class directly. Access it via the loader attribute
    of the [SentioProber](SentioProber.md) class.
    """

    def __init__(self, parent : CommandGroupBase) -> None:
        super().__init__(parent)


    def list(self) -> List[str]:
        """List all virtual carriers defined in SENTIO.

        Wraps Sentios "loader:vc:list" remote command.

        Returns:
            carriers (Tuple[str]): A tuple with the names of the virtual carriers.
        """

        try:
            self.comm.send("loader:vc:list")
            resp = Response.check_resp(self.comm.read_line())
            
            list : List[str] = resp.message().split(',')
            return list
        except:
            return []
        

    def select(self, vc_name : str) -> None:
        """Select a virtual carrier.

        Wraps Sentios "loader:vc:select" remote command.

        Args:
            vc_name (str): The name of the virtual carrier to select.

        Returns:
            None
        """

        resp : Response = self.prober.send_cmd(f"loader:vc:select {vc_name}")
        resp.check()


    def initialize(self, carrier_name : str, mode : VirtualCarrierInitFlags = VirtualCarrierInitFlags.Start, forceDataSync : bool = False, timeout : int = 90) -> List[Tuple[VirtualCarrierStepProcessingState, str, LoaderStation, int, float, int]]:
        """Initializes the selected virtual carrier.
        
            Wraps Sentios "loader:vc:start_initialize" remote command. This command synchronizes the async
            start_initialize command with a wait_complete command.

            Args:
                carrier_name (str): The name of the virtual carrier to initialize. This carrier will be made SENTIO's active carrier.
                continue_process (bool): A boolean flag to indicate if a previous virtual carrier measurement shall be continued. (default is False)
                timeout (int): The timeout in seconds. (default is 90 seconds)

            Returns:
                A List of steps to execute.
        """

        resp : Response = self.prober.send_cmd(f"loader:vc:start_initialize {carrier_name},{mode.toSentioAbbr()},{forceDataSync}")
        resp = self.prober.wait_complete(resp.cmd_id())

        # parse processing steps into a list of tuples
        steps : List[Tuple[VirtualCarrierStepProcessingState, str, LoaderStation, int, float, int]] = []

        steps_as_str : List[str] = Helper.split_string(resp.message(), ',')
#        steps_as_str : List[str] = resp.message().split(',')

        for it in steps_as_str:
#            col = it.split(' ')
            col = Helper.split_string(it, ' ')

            state = VirtualCarrierStepProcessingState[col[0]]
            id = col[1]
            station = LoaderStation[col[2]]
            slot = int(col[3])
            temp = float(col[4])
            probecard_idx = int(col[5])
            steps.append((state, id, station, slot, temp, probecard_idx))

        return steps


    def next_step(self, timeout : int = 120) -> Tuple[VirtualCarrierStepProcessingState, str, LoaderStation, int, float, int]:
        """Execute the next processing step of the virtual carrier.

            Wraps Sentios "loader:vc:start_next_step" remote command.

        Returns:
            A tuple with the processing step information.
        """

        resp : Response = self.prober.send_cmd("loader:vc:start_next_step")
        resp = self.prober.wait_complete(resp, timeout)

        col = resp.message().split(',')
        state = VirtualCarrierStepProcessingState[col[0]]
        id = col[1]
        station = LoaderStation[col[2]]
        slot = int(col[3])
        temp = float(col[4])
        probecard_idx = int(col[5])

        return (state, id, station, slot, temp, probecard_idx)
    

    def save_state(self) -> None:
        """ Save the state of the currently active virtual carrier.

            Wraps Sentios "loader:vc:save_state" remote command.

        Returns:
            None
        """
        
        resp : Response = self.prober.send_cmd("loader:vc:save_state")
        resp.check()


