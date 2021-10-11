from sentio_prober_control.Sentio.ProberBase import ProberException


class Response:
    def __init__(self, errc: int, stat: int, cmd_id: int, msg: str):
        self.__errc = errc
        self.__stat = stat
        self.__cmd_id = cmd_id
        self.__msg = msg

    @staticmethod
    def parse_resp(resp):
        tok = resp.split(",", 2)

        # split response items
        errc = int(tok[0]) & 1023              # lowermost 10 bits are the error code
        stat = (int(tok[0]) & ~1023) >> 10     # everything from bit 10 on is the status

        cmd_id = int(tok[1])
        msg = tok[2].rstrip()

        # seperate error code an status code
        resp = Response(errc, stat, cmd_id, msg)
        #resp.dump()
        return resp

    @staticmethod
    def check_resp(str_resp):
        resp = Response.parse_resp(str_resp)
        if not resp.ok():
            raise ProberException(resp.message(), resp.errc())

        return resp

    def check(self):
        if not self.ok():
            raise ProberException(self.message(), self.errc())

    def cmd_id(self) -> int:
        return self.__cmd_id

    def errc(self) -> int:
        return self.__errc

    def message(self) -> str:
        return self.__msg

    def status(self):
        return self.__stat

    def ok(self) -> str:
        return self.__errc == 0

    def check_error(self):
        if not self.ok():
            raise ProberException(self.resp.message(), self.resp.errc())
    
    def dump(self):
        print("errc={0}; stat={1}; msg=\"{2}\"; id={3}".format(self.__errc, self.__stat, self.__msg, self.__cmd_id))
