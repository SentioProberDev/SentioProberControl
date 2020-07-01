from abc import ABC

from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Response import *

class ModuleCommandGroupBase(CommandGroupBase):
    def __init__(self, comm, abbr):
        super().__init__(comm)
        self._groupAbbr = abbr

    def get_prop(self, prop_name: str, arg1=None):
        if arg1 == None:
            self._comm.send("{0}:get_prop {1}".format(self._groupAbbr, prop_name))
        else:
            self._comm.send("{0}:get_prop {1}, {2}".format(self._groupAbbr,prop_name, arg1))

        resp = Response.check_resp(self._comm.read_line())

        values = resp.message().split(',')

        # Try to figure out the type of the return value
        if (len(values) == 1):
            # Test 1: Check if the returned value is a boolean. Do not use bool(...) because this
            #         would also convert numeric values
            if resp.message().lower()=='true' or resp.message().lower()=='false':
                val = bool(resp.message())
                return val

            # Test 2: Try to convert the return value into a number
            try:
                # I cannot distinguish between int and float reliably. Values will always be returned as floats
                val = float(resp.message())
                return val
            except:
                return resp.message()
        elif len(values) == 2:
            return float(values[0]), float(values[1])
        elif len(values) == 3:
            return float(values[0]), float(values[1]), float(values[2])

        return int(resp.message())

    def set_prop(self, prop_name: str, *argv):
        cmd: str = self._groupAbbr + ':set_prop {0}'
        for n in range(0, len(argv)):
            cmd += ', {0}'.format(argv[n])

        self._comm.send(cmd.format(prop_name))
        Response.check_resp(self._comm.read_line())