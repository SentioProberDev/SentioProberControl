import ctypes
import re
from ctypes import *


class GpibNiDriver:

    def __init__(self):
        # load gpib dll
        gpibDll = ctypes.WinDLL("ni4882.dll")

        # gpib init functions
        self._gpibSendIfc = gpibDll.SendIFC
        self._gpibSendIfc.argtypes = [c_int]

        self._gpibThreadIbsta = gpibDll.ThreadIbsta
        self._gpibThreadIbsta.restype = c_int

        self._gpibThreadIberr = gpibDll.ThreadIberr
        self._gpibThreadIberr.restype = c_int

        self._gpibThreadIbcnt = gpibDll.ThreadIbcnt
        self._gpibThreadIbcnt.restype = c_int

#        self._gpibIbfind = gpibDll.ibfindW
#        self._gpibIbfind.restype = c_int
#        self._gpibIbfind.argtypes = [c_wchar_p]

        self._gpibIbsic = gpibDll.ibsic
        self._gpibIbsic.restype = c_int
        self._gpibIbsic.argtypes = [c_int]

        # gpib send
        self._gpibSendImpl = gpibDll.Send
        self._gpibSendImpl.argtypes = [c_int, c_ushort, c_char_p, c_int, c_int]

        # gpib receive
        self._gpibReceiveImpl = gpibDll.Receive
        self._gpibReceiveImpl.argtypes = [c_int, c_ushort, c_void_p, c_int, c_int]


    def connect(self, board_name: str, address: int):
        # init
        numbers = re.findall('[0-9]+', board_name)
        self._board = int(numbers[0])

        self._gpibSendIfc(self._board)

        self._addr = address
        self._max_len = 1000


    def get_globals(self):
        ibsta = self._gpibThreadIbsta()
        iberr = self._gpibThreadIberr()
        ibcnt = 0
        ibcntl = self._gpibThreadIbcnt()

        return ibsta, iberr, ibcnt, ibcntl

    def send(self, str):
        self._gpibSendImpl(self._board, self._addr, str.encode('utf-8'), len(str), 1)

    def receive(self):
        byteArr = (c_byte * self._max_len)()
        self._gpibReceiveImpl(self._board, self._addr, byteArr, self._max_len, 0)
        ibsta, iberr, ibcnt, ibcntl = self.get_globals()
        return bytearray(byteArr[:ibcntl]).decode("utf-8")