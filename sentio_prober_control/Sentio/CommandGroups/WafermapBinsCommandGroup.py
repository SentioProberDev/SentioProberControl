from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase
from sentio_prober_control.Sentio.Enumerations import *


class WafermapBinsCommandGroup(CommandGroupBase):
    """ This command group bundles functions for setting up and using the binning table of the wafermap. """


    def clear_all(self) -> None:
        """ Clear all bins. Remove the bin code from all dies and sibsites.
        """
        self._comm.send("map:bins:clear_all")
        Response.check_resp(self._comm.read_line())


    def clear_all_values(self) -> None:
        """  Removes all temporarily stored values from the dies.

            Each die can store a single floating point value. This value can be used for 
            visualizing parameters across the wafer. 
        """
        self._comm.send("map:bins:clear_all_values")
        Response.check_resp(self._comm.read_line())


    def load(self, file: str) -> None:
        """ Load a binning table from file.
         
            Wraps SENTIO's map:bins:load remote command.

            Args:
                file: The file to load the binning table from.
        """
        self._comm.send(f"map:bins:load {file}")
        Response.check_resp(self._comm.read_line())


    def set_all(self, bin_val: int, selection: BinSelection) -> None:
        """  Sets the bins of all dies on the wafermap to a specific value. 
        
            Wraps SENTIO's map:bins:set_all remote command.

            Args:
                bin_val: The bin value to set.
                selection: The selection of dies to set the bin value for.
        """
        self._comm.send(f"map:bins:set_all {bin_val}, {selection.toSentioAbbr()}")
        Response.check_resp(self._comm.read_line())#


    def set_bin(self, bin_value: int, col: int, row: int, site : int = None) -> None:
        """ Set a single bin.

            Wraps SENTIO's map:bins:set_bin remote command.

            Args:
                bin_value: The bin value to set.
                col: The column of the die.#
                row: The row of the die.
                site: The site of the die.
        """
        if site is None:
            self._comm.send(f"map:bins:set_bin {bin_value}, {col}, {row}")
        else:
            self._comm.send(f"map:bins:set_bin {bin_value}, {col}, {row}, {site}")

        Response.check_resp(self._comm.read_line())


    def set_value(self, value: float, col: int, row: int)->None:
        """ Set a value on a single die.

            Args:
                value: The value to set.
                col: The column of the die.
                row: The row of the die. 
         """
        self._comm.send("map:bins:set_value {0}, {1}, {2}".format(value, col, row))
        Response.check_resp(self._comm.read_line())