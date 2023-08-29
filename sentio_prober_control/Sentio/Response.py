from sentio_prober_control.Sentio.ProberBase import ProberException


class Response:
    """ This class represents the response of a single SENTIO remote command. 
    
        Sentio's remote command response is a comma separated string that contains three fields
        which represent 4 data items. (error code and status code are combined)

        :param errc: The error code.
        :param stat: The status code.
        :param cmd_id: The async command id. (only used by async commands)
        :param msg: The response message.
    """
    def __init__(self, errc: int, stat: int, cmd_id: int, msg: str):
        """ Creates a new Response object. """
        self.__errc = errc
        self.__stat = stat
        self.__cmd_id = cmd_id
        self.__msg = msg

    @staticmethod
    def parse_resp(resp):
        """ A static method that parses a SENTIO remote command response string and returns a Response object.

            A typical response from SENTIO to a remote command might look like "0,0,ok"
            SENTIO's remote command responses are strings that contain multiple items
            separated by two commas. 

            - error code and status information (combined in one integer)
            - an async command id (only used by async commands)
            - a response message

            :return: A Response object created from the information in SENTIO's response string.
        """
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
    def check_resp(str_resp : str):
        """ A static method that parses a response string and raises an exception if the response indicates an error. 
            
            :param str_resp: The response string to parse.
            :return: A Response object created from the information in SENTIO's response string.
            :raises: ProberException if the response indicates an error.
        """
        resp = Response.parse_resp(str_resp)
        if not resp.ok():
            raise ProberException(resp.message(), resp.errc())

        return resp

    def check(self):
        """ Raises an exception if this response indicates an error."""
        if not self.ok():
            raise ProberException(self.message(), self.errc())

    def check_error(self):
        # ibg: I dont think this code works. it is a duplicate of check() and it is either outdated or never worked.
        if not self.ok():
            raise ProberException(self.resp.message(), self.resp.errc())

    def cmd_id(self) -> int:
        """ The async commans id returned by SENTIO. 
        
            If the remote command is not an async command 0 is returned.

            :return: The async command id returned by SENTIO.
        """
        return self.__cmd_id

    def errc(self) -> int:
        """ The error code returned by SENTIO. 

            The meaning of the error code is documented in the SENTIO's remote command documentation.
            It is also used by the enumerator RemoteCommandError.

            :return: The error code returned by SENTIO.
        """
        return self.__errc

    def message(self) -> str:
        """ The response message returned by SENTIO.
            :return: The response message returned by SENTIO.
        """
        return self.__msg

    def status(self):
        """ The status coode extracted from the response.
            :return: The status code returned by SENTIO.
        """
        return self.__stat

    def ok(self) -> str:
        """ Returns True if the response indicates no error."""
        return self.__errc == 0

    def dump(self):
        """ Prints the content of the response object to the console.
        
            Used for debugging purposes.
        """
        print("errc={0}; stat={1}; msg=\"{2}\"; id={3}".format(self.__errc, self.__stat, self.__msg, self.__cmd_id))
