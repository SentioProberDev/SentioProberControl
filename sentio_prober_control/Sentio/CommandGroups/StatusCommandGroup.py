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


    def set_chuck_temp(self, temp: float) -> Response:
        """Set chuck temperature setpoint.

        Args:
            temp: The chuck temperature setpoint in degrees Celsius.
        """

        self.comm.send(f"status:set_chuck_temp {temp:.2f}")
        return Response.check_resp(self.comm.read_line())
