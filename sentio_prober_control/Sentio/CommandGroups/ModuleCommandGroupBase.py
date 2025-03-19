from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class ModuleCommandGroupBase(CommandGroupBase):
    """Base class for all command groups."""

    def __init__(self, parent : 'SentioProber', abbr) -> None:
        super().__init__(parent)
        self._groupAbbr = abbr


    def get_prop(self, prop_name: str, arg1=None):
        """Query a module property.

        SENTIO exposes some of its internal variables in the form of so called "module properties".
        Module properties represent values that are identified by their name and can be of different
        types.

        A module property can also have an additional parameter.

        The remote command specification contains a list of some of exposed module properties.

        :param prop_name: The name of the property to query.
        :param arg1: An optional parameter for the property.
        :raises: ProberException if an error occured.
        """
        if arg1 == None:
            self.comm.send("{0}:get_prop {1}".format(self._groupAbbr, prop_name))
        else:
            self.comm.send("{0}:get_prop {1}, {2}".format(self._groupAbbr, prop_name, arg1))

        resp = Response.check_resp(self.comm.read_line())

        values = resp.message().split(",")

        # Try to figure out the type of the return value
        if len(values) == 1:
            # Test 1: Check if the returned value is a boolean. Do not use bool(...) because this
            #         would also convert numeric values
            #
            if resp.message().lower() == "true":
                return True
            elif resp.message().lower() == "false":
                return False

            # Test 2: Try to convert the return value into a number
            try:
                # I cannot distinguish between int and float reliably. Values will always be returned as floats
                return float(resp.message())
            except:
                return resp.message()
        elif len(values) == 2:
            return float(values[0]), float(values[1])
        elif len(values) == 3:
            return float(values[0]), float(values[1]), float(values[2])

        return int(resp.message())


    def set_prop(self, prop_name: str, *argv):
        """Set a module property.

        SENTIO exposes some of its internal variables in the form of so called "module properties".
        Module properties represent values that are identified by their name and can be of different
        types.

        A module property can also have an additional parameter.

        The remote command specification contains a list of some of exposed module properties.

        :param prop_name: The name of the property to query.
        :param argv: Optional parameters for the property.
        :raises: ProberException if an error occured.
        """
        cmd: str = self._groupAbbr + ":set_prop {0}"
        for n in range(0, len(argv)):
            cmd += ", {0}".format(argv[n])

        self.comm.send(cmd.format(prop_name))
        Response.check_resp(self.comm.read_line())
