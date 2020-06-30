from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *
from typing import Tuple
import time

class VisionIMagProCommandGroup(CommandGroupBase):
    def __init__(self, comm):
        super().__init__(comm)

    """ Move imagpro's internal z-axis """
    def move_z(self, ref: IMagProZReference, pos: float ):
        #
        # the imag pro axis is showing hysteresis behavior. z position seems to be only
        # reproducable when the axis is moved from one of its endpoints! If you remove
        # the next three lines. The z-position will become very inaccurate!
        #
        #self._comm.send("vis:imagpro:move_z center, -1000")
        #Response.check_resp(self._comm.read_line())
        #time.sleep(0.5)

        self._comm.send("vis:imagpro:move_z {0}, {1}".format(ref.toSentioAbbr(), pos))
        resp = Response.check_resp(self._comm.read_line())
        #time.sleep(0.5)
        return float(resp.message())

    """ Get the position od imagpro's internal axis """
    def get_z(self, ref: IMagProZReference):
        par:str = ref.toSentioAbbr()
        self._comm.send("vis:imagpro:get_z {0}".format(par))
        resp = Response.check_resp(self._comm.read_line())
        return float(resp.message())

    """ Get the xy compensation value for a certain z-position of imagpro's internal axis 
    
        !!! UNTESTED !!!
    """
    def get_xy_comp(self, imag_pro_z: float):
        self._comm.send("vis:imagpro:get_xy_comp {0}".format(imag_pro_z))

        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])
