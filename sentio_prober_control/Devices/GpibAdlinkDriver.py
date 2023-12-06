""" @private """

import ctypes
from ctypes import byref, c_byte, c_char_p, c_int, c_ushort, c_void_p, c_wchar_p


class GpibAdlinkDriver:
    """A python wrapper for the ADLINK gpib-32.dll.

    This class is used internally only.

    @private
    """

    def __init__(self):
        # load gpib dll
        gpibDll = ctypes.WinDLL("gpib-32.dll")

        # gpib init functions
        self._gpibIbfind = gpibDll.ibfindW
        self._gpibIbfind.restype = c_int
        self._gpibIbfind.argtypes = [c_wchar_p]

        self._gpibIbrsc = gpibDll.ibrsc
        self._gpibIbrsc.restype = c_int
        self._gpibIbrsc.argtypes = [c_int, c_int]

        self._gpibIbsic = gpibDll.ibsic
        self._gpibIbsic.restype = c_int
        self._gpibIbsic.argtypes = [c_int]

        # gpib send
        self._gpibSendImpl = gpibDll.Send
        self._gpibSendImpl.argtypes = [c_int, c_ushort, c_char_p, c_int, c_int]

        # gpib receive
        self._gpibReceiveImpl = gpibDll.Receive
        self._gpibReceiveImpl.argtypes = [c_int, c_ushort, c_void_p, c_int, c_int]

        # gpib receive
        self._gpibGetGlobalsImpl = gpibDll.gpib_get_globals
        self._gpibGetGlobalsImpl.restype = c_int
        self._gpibGetGlobalsImpl.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]

    def connect(self, board_name: str, address: int):
        # init
        self._board = self._gpibIbfind(board_name)  # "GPIB0")
        if self._board < 0:
            raise Exception(f"Board {board_name} does not exist!")

        self._gpibIbrsc(self._board, 1)
        self._gpibIbsic(self._board)

        self._addr = address
        self._max_len = 1000

    def get_globals(self):
        ibsta = c_int()
        iberr = c_int()
        ibcnt = c_int()
        ibcntl = c_int()
        self._gpibGetGlobalsImpl(
            byref(ibsta), byref(iberr), byref(ibcnt), byref(ibcntl)
        )
        return ibsta.value, iberr.value, ibcnt.value, ibcntl.value

    def send(self, str):
        self._gpibSendImpl(self._board, self._addr, str.encode("utf-8"), len(str), 1)

    def receive(self):
        byteArr = (c_byte * self._max_len)()
        self._gpibReceiveImpl(self._board, self._addr, byteArr, self._max_len, 0)
        ibsta, iberr, ibcnt, ibcntl = self.get_globals()
        return bytearray(byteArr[:ibcntl]).decode("utf-8")
