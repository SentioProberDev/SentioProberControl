from deprecated import deprecated

from sentio_prober_control.Sentio.ProberBase import ProberException


class Response:
    """This class represents the response of a single SENTIO remote command.

    Sentio's remote command response is a comma separated string that contains three fields
    which represent 4 data items. (error code and status code are combined)

    """

    def __init__(self, errc: int, stat: int, cmd_id: int, msg: str):
        """Creates a new Response object.

        Args:
            errc (int): The error code.
            stat (int): The status code.
            cmd_id (int): The async command id. (only used by async commands)
            msg (str): The response message.
        """
        self.__errc = errc
        self.__stat = stat
        self.__cmd_id = cmd_id
        self.__msg = msg


    @staticmethod
    def parse_resp(resp):
        """A static method that parses a SENTIO remote command response string and returns a Response object.

        A typical response from SENTIO to a remote command might look like "0,0,ok"
        SENTIO's remote command responses are strings that contain multiple items
        separated by two commas.

        - error code and status information (combined in one integer)
        - an async command id (only used by async commands)
        - a response message

        Returns:
            response (Resppnse): A Response object created from the information in SENTIO's response string.
        """
        tok = resp.split(",", 2)

        # split response items
        errc = int(tok[0]) & 1023  # lowermost 10 bits are the error code
        stat = (int(tok[0]) & ~1023) >> 10  # everything from bit 10 on is the status

        cmd_id = int(tok[1])
        msg = tok[2].rstrip()

        # seperate error code an status code
        resp = Response(errc, stat, cmd_id, msg)
        # resp.dump()
        return resp
    

    @staticmethod
    def check_resp(str_resp: str) -> "Response":
        """A static method that parses a response string and raises an exception if the response indicates an error.

        Args:
            str_resp (str): The response string to parse.

        Returns:
            response (Response): A Response object created from the information in SENTIO's response string. If the response represents
                                 an error an exception is raised instead of returning a Response object.

        Raises:
            ProberException: If the response indicates an error.
        """
        resp = Response.parse_resp(str_resp)
        if not resp.ok():
            raise ProberException(resp.message(), resp.errc())

        return resp


    def check(self):
        """Raises an exception if this response indicates an error.

        Raises:
            ProberException: If the response indicates an error.
        """
        if not self.ok():
            raise ProberException(self.message(), self.errc())


    def cmd_id(self) -> int:
        """The async commans id returned by SENTIO.

        If the remote command is not an async command 0 is returned.

        Returns:
            cmd_id (int): The async command id returned by SENTIO.
        """
        return self.__cmd_id


    def errc(self) -> int:
        """The error code returned by SENTIO.

        The meaning of the error code is documented in the SENTIO's remote command documentation.
        It is also used by the enumerator RemoteCommandError.

        Returns:
            errc (int): The error code returned by SENTIO.
        """
        return self.__errc


    def message(self) -> str:
        """The response message returned by SENTIO.

        Returns:
            msg (str): The response message returned by SENTIO.
        """
        return self.__msg


    def status(self):
        """The status coode extracted from the response.

        Returns:
            stat (int): The status code returned by SENTIO.
        """
        return self.__stat


    def ok(self) -> bool:
        """Returns True if the response indicates no error.

        Returns:
            ok (bool): True if the response indicates no error, False otherwise.
        """
        return self.__errc == 0


    @deprecated("Use print() instead")
    def dump(self) -> None:
        print('errc={0}; stat={1}; msg="{2}"; id={3}'.format(self.__errc, self.__stat, self.__msg, self.__cmd_id))


    def print(self) -> None:
        """Prints the content of the response object to the console."""
        print('errc={0}; stat={1}; msg="{2}"; id={3}'.format(self.__errc, self.__stat, self.__msg, self.__cmd_id))
