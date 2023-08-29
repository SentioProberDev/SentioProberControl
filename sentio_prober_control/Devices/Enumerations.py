from enum import Enum


class GpibCardVendor(Enum):
    """ Specifies the vendor of the GPIB card. """    
    Adlink = 0,
    """ Specify this if you use an ADLINK GPIB card. """
    NationalInstruments = 1
    """ Specify this if you use a National Instruments GPIB card."""
