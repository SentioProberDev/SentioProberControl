from typing import Tuple

from sentio_prober_control.Sentio.Enumerations import BinSelection, BinQuality
from sentio_prober_control.Sentio.Response import Response
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import CommandGroupBase


class WafermapBinsCommandGroup(CommandGroupBase):
    """This command group bundles functions for setting up and using the binning table of the wafermap."""

    def clear_all(self) -> None:
        """Clear all bins. Remove the bin code from all dies and sibsites."""
        self.comm.send("map:bins:clear_all")
        Response.check_resp(self.comm.read_line())


    def clear_all_values(self) -> None:
        """Removes all temporarily stored values from the dies.

        Each die can store a single floating point value. This value can be used for
        visualizing parameters across the wafer.
        """
        self.comm.send("map:bins:clear_all_values")
        Response.check_resp(self.comm.read_line())


    def get_bin(self, col: int | None = None, row: int | None = None, site: int | None = None) -> int:
        """Get the bin information of a die or a subsite.

        Wraps SENTIO's map:bins:get_bin remote command.

        Args:
            col: The column of the die.
            row: The row of the die.
            site: The site of the die.

        Returns:
            The bin value of the die or subsite.
        """
        if col is None and row is None and site is None:
            self.comm.send(f"map:bins:get_bin")
        elif site is None and col is not None and row is not None:
            self.comm.send(f"map:bins:get_bin {col}, {row}")
        elif site is not None and col is not None and row is not None:
            self.comm.send(f"map:bins:get_bin {col}, {row}, {site}")
        else:
            raise ValueError("get_bin command requires either no parameter or column and row or column, row and site.")
        
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())


    def get_bin_info(self, bin : int) -> Tuple[int, str, BinQuality, str]:
        """Get the information of a bin code from the binning table defined in the wafer map.
        
            Wraps SENTIO's map:bins:get_bin_info remote command.

            Returns:
                A tuple containing the following data items: bin index (same value as the argument), bin description, bin quality (pass/fail information) and bin color.
        """
        self.comm.send(f"map:bins:get_bin_info {bin}")        
        resp = Response.check_resp(self.comm.read_line())

        values = resp.message().split(",")
        return int(values[0]), values[1], BinQuality[values[2]], values[3]
    

    def get_num_bins(self) -> int:
        """Get the number of bins in the binning table.
        
            Returns:
                The number of bins in the binning table.
        """
        self.comm.send("map:bins:get_num_bins")
        resp = Response.check_resp(self.comm.read_line())
        return int(resp.message())
    

    def load(self, file: str) -> None:
        """Load a binning table from file.

        Wraps SENTIO's map:bins:load remote command.

        Args:
            file: The file to load the binning table from.
        """
        self.comm.send(f"map:bins:load {file}")
        Response.check_resp(self.comm.read_line())


    def set_all(self, bin_val: int, selection: BinSelection) -> None:
        """Sets the bins of all dies on the wafermap to a specific value.

        Wraps SENTIO's map:bins:set_all remote command.

        Args:
            bin_val: The bin value to set.
            selection: The selection of dies to set the bin value for.
        """
        self.comm.send(f"map:bins:set_all {bin_val}, {selection.toSentioAbbr()}")
        Response.check_resp(self.comm.read_line())  #


    def set_bin(self, bin_value: int, col: int | None = None, row: int | None = None, site: int | None = None) -> None:
        """Set a single bin.

        Wraps SENTIO's map:bins:set_bin remote command.

        Args:
            bin_value: The bin value to set.
            col: The column of the die.#
            row: The row of the die.
            site: The site of the die.
        """
        if col is None and row is None and site is None:
            self.comm.send(f"map:bins:set_bin {bin_value}")
        elif site is None and col is not None and row is not None:
            self.comm.send(f"map:bins:set_bin {bin_value}, {col}, {row}")
        elif site is not None and col is not None and row is not None:
            self.comm.send(f"map:bins:set_bin {bin_value}, {col}, {row}, {site}")
        else:
            raise ValueError("set_bin command requires either no parameter or column and row or column, row and site.")

        Response.check_resp(self.comm.read_line())


    def set_value(self, value: float, col: int, row: int) -> None:
        """Set a value on a single die.

        Args:
            value: The value to set.
            col: The column of the die.
            row: The row of the die.
        """
        self.comm.send("map:bins:set_value {0}, {1}, {2}".format(value, col, row))
        Response.check_resp(self.comm.read_line())
