import socket

from Mpi.Communication.CommunicatorBase import CommunicatorBase;


class CommunicatorTcpIp(CommunicatorBase):
    def __init__(self):
        self.__socket = socket.socket()

    @staticmethod
    def create(addr: str):
        c = CommunicatorTcpIp()
        c.connect(addr)
        return c

    def connect(self, address: str):
        tok = address.split(":")
        self.__address = tok[0]
        self.__port = int(tok[1])

        if CommunicatorBase._verbose:
            print("Connecting comunicator to {0}:{1}".format(self.__address, self.__port))

        self.__socket.connect((self.__address, self.__port))

    def disconnect(self):
        if CommunicatorBase._verbose:
            print("Diconnecting comunicator to {0}".format(self.__address))

        self.__socket.close()

    def send(self, msg: str):
        if CommunicatorBase._verbose:
            print("Sending \"{0}\"".format(msg))

        self.__socket.send((msg + "\n").encode())

    def read_line(self):
        return self.__socket.makefile().readline().rstrip()

