from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import ThermoChuckState
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import (
    ModuleCommandGroupBase,
)


class StatusCommandGroup(ModuleCommandGroupBase):
    """A command group for getting the status of the probe station and controlling the dashboard module."""

    def __init__(self, comm) -> None:
        super().__init__(comm, "status")


    def get_chuck_temp(self) -> float:
        """Get current chuck temperature.

        Returns:
            The chuck temperature in degrees Celsius.
        """

        self.comm.send("status:get_chuck_temp")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        temp = float(tok[0])
        return temp


    def get_chuck_temp_setpoint(self) -> float:
        """Get current chuck temperature setpoint.

        Returns:
            The chuck temperature setpoint in degrees Celsius.
        """

        self.comm.send("status:get_chuck_temp_setpoint")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        temp = float(tok[0])
        return temp


    def get_chuck_thermo_state(self) -> ThermoChuckState:
        """Return thermo chuck state.

        Returns:
            A tuple with the current state of the thermo chuck. Contains six boolean variables:
            isCooling, isHeating, isControlling, isStandby, isError, isUncontrolled.
        """

        self.comm.send("status:get_chuck_thermo_state")
        resp = Response.check_resp(self.comm.read_line())

        if "soaking" in resp.message().lower():
            return ThermoChuckState.Soaking
        elif "cooling" in resp.message().lower():
            return ThermoChuckState.Cooling
        elif "heating" in resp.message().lower():
            return ThermoChuckState.Heating
        elif "controlling" in resp.message().lower():
            return ThermoChuckState.Controlling
        elif "standby" in resp.message().lower():
            return ThermoChuckState.Standby
        elif "error" in resp.message().lower():
            return ThermoChuckState.Error
        elif "uncontrolled" in resp.message().lower():
            return ThermoChuckState.Uncontrolled
        else:
            return ThermoChuckState.Unknown


    def get_machine_status(self) -> Tuple[bool, bool, bool]:
        """Get machine status.

        Returns:
            A tuple with the current status of the machine. Contains three boolean variables: isInitialized, isMeasuring, LoaderBusy.
        """

        self.comm.send("status:get_machine_status")
        resp = Response.check_resp(self.comm.read_line())
        tok = resp.message().split(",")
        isInitialized = "Ready" in tok
        isMeasuring = "IsMeasuring" in tok
        LoaderBusy = "LoaderBusy" in tok
        return isInitialized, isMeasuring, LoaderBusy


    def get_soaking_time(self, temperature: float):
        """Get the thermochuck soaking time in seconds that is set up for a certain temperature in the dashboard.

        Args:
            temperature: The temperature. This temperature value must be one of the predefined temperature
                  values set up in the dashboard.

        Raises:
            ProberException: With error code 200 is thrown when the temperature is not a predefined value set up in the dashboard.
            May also raise an an exception when other errors occur.

        Returns:
            The soaking time in seconds.
        """

        self.comm.send(f"status:get_soaking_time {temperature:.2f}")
        resp = Response.check_resp(self.comm.read_line())
        temp = float(resp.message())
        return temp


    def set_chuck_temp(self, temp: float, lift_chuck : bool = False) -> None:
        """Set chuck temperature setpoint.

            This function wraps SENTIO's status:set_chuck_temp remote command.

            Args:
                temp: The chuck temperature setpoint in degrees Celsius.
                lift_chuck: If True, the chuck will moved to the lift position if required. If this value is false and a move to lift is required an error occurs.

            Raises:
                ProberException: If an error occurred.
        """
        self.comm.send(f"status:set_chuck_temp {temp:.2f}, {lift_chuck}")
        Response.check_resp(self.comm.read_line())
    
    def get_chuck_thermo_energy_mode(self) -> str:
        """Get the current chuck thermo energy mode.
        Returns:
            The current energy mode as a string. Possible values: Fast, Optimal, HighPower, Customized.
        """
        self.comm.send("status:get_chuck_thermo_energy_mode")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def get_chuck_thermo_hold_mode(self) -> str:
        """Get thermo chuck hold mode.

        Returns:
            The current hold mode. Possible values: Active, Nonactive.
        """
        self.comm.send("status:get_chuck_thermo_hold_mode")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def get_high_purge_state(self) -> str:
        """Get thermo chuck high purge state.

        Returns:
            The current high purge state. Possible values: ON, OFF.
        """
        self.comm.send("status:get_high_purge_state")
        resp = Response.check_resp(self.comm.read_line())
        return resp.message()
    
    def set_chuck_thermo_energy_mode(self, mode: str) -> Response:
        """Set chuck thermo energy mode.

        Args:
            mode: The desired energy mode. Possible values: Fast, Optimal, HighPower, Customized.

        Returns:
            A Response object confirming the command execution.

        Raises:
            ValueError: If the provided mode is not valid.
        """
        self.comm.send(f"status:set_chuck_thermo_energy_mode {mode}")
        return Response.check_resp(self.comm.read_line())
    
    def set_chuck_thermo_hold_mode(self, mode: bool) -> Response:
        """Set thermo chuck hold mode.

        Args:
            mode: A boolean indicating whether to enable (True) or disable (False) hold mode.

        Returns:
            A Response object confirming the command execution.
        """
        self.comm.send(f"status:set_chuck_thermo_hold_mode {mode}")
        return Response.check_resp(self.comm.read_line())
    
    def set_chuck_thermo_mode(self, mode: str) -> Response:
        """Set chuck thermo operation mode.

        Args:
            mode: The operation mode to set. Possible values: Normal, Standby, Defrost, Purge, Turbo, Eco.

        Returns:
            A Response object confirming the command execution.

        Raises:
            ValueError: If the provided mode is not valid.
        """
        self.comm.send(f"status:set_chuck_thermo_mode {mode}")
        return Response.check_resp(self.comm.read_line())

    def set_high_purge(self, enable: bool) -> Response:
        """Set thermo chuck high purge state.

                Args:
                    enable: A boolean indicating whether to enable (True) or disable (False) high purge.

                Returns:
                    A Response object confirming the command execution.
                """
        self.comm.send(f"status:set_high_purge {enable}")
        return Response.check_resp(self.comm.read_line())