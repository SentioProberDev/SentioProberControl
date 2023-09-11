from typing import Tuple
from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *

class ProbeCommandGroup(CommandGroupBase):
    """ This command group contains functions for working with motorized prober. 
    
        Do not instantiate this class directly. Access it via the probe member of the prober class.
    """

    def __init__(self, comm):
        """ Initialize the command group. 
            
            You are not supposed to instantiate this class directly. Use the Prober class instead.

            Example:
            >>> from sentio_prober_control.Sentio.ProberSentio import *
            >>> prober = SentioProber.create_prober("tcpip", "127.0.0.1:35555")
            >>> prober.probe.move_probe_xy(ProbeSentio.East, ProbeXYReference.Current, 1000, 2000)


            :param comm: The communication object to use for sending the commands.
        """

        self.__comm = comm


    def async_step_probe_site(self, probe: ProbeSentio, idx: int )  -> int:
        """ Start the process of stepping to a positioner site. 
         
            Each positioner can define n a number of predefined positions called "sites". This command
            initiates a step to such a site. This is an asynchronous command use in conjunction with 
            ProberSentio.wait_complete() or ProberSentio.query_command_status().

            :param probe: The probe to step.
            :param idx: The index of the site to step to.
            :raises ProberException: if the command could not be executed successfully.
            :return: The async command id of the command. 
        """

        self.__comm.send("start_step_positioner_site {0},{1}".format(probe.toSentioAbbr(), idx))
        resp = Response.check_resp(self.__comm.read_line())
        return resp.cmd_id()


    def async_step_probe_site_next(self, probe: ProbeSentio)  -> int:
        """ Step to next probe site. 
        
            Each positioner can define n a number of predefined positions called "sites".
            This command initiates a step to the next site. This is an asynchronous command 
            use in conjunction with ProberSentio.wait_complete() or ProberSentio.query_command_status().

            :param probe: The probe to step.
            :raises ProberException: if the command could not be executed successfully.
            :return: The async command id of the command.
        """

        self.__comm.send("start_step_positioner_site_next {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return resp.cmd_id()


    def async_step_probe_site_first(self, probe: ProbeSentio)  -> int:
        """ Step to first probe site. 
        
            Each positioner can define n a number of predefined positions called "sites".
            This command initiates a step to the first site. This is an asynchronous command
            use in conjunction with ProberSentio.wait_complete() or ProberSentio.query_command_status().

            :param probe: The probe to step.
            :raises ProberException: if the command could not be executed successfully.
            :return: The async command id of the command.
        """

        self.__comm.send("start_step_positioner_site_first {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return resp.cmd_id()
    

    def get_probe_site(self, probe: ProbeSentio, idx: int ) -> Tuple[int, str, float, float]:
        """ Get information for a probe site. 
        
            Each positioner can define n a number of predefined positions called "sites".
            This command returns the data associated with a site.

            :param probe: The probe to get the site for.
            :raises ProberException: if the command could not be executed successfully.
            :return: A tuple containing the site index, the site name, the x position in micrometer and the y position in micrometer.
        """
        self.__comm.send("get_positioner_site {0},{1}".format(probe.toSentioAbbr(), idx))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")

        return int(tok[0]), str(tok[1]), float(tok[2]), float(tok[3])


    def get_probe_site_number(self, probe: ProbeSentio) -> int:
        """ Returns the total number of probe sites set up. 
        
            Each positioner can define n a number of predefined positions called "sites".
            This command returns the total number of sites.

            :raises ProberException: if the command could not be executed successfully.
            :return: The total number of sites.
        """

        self.__comm.send("get_positioner_site_num {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return int(resp.message())



    def get_probe_xy(self, probe: ProbeSentio, ref: ProbeXYReference) -> Tuple[float, float]:
        """ Get probe xy position in micrometer.

            :param probe: The probe to get the position for.
            :param ref: The position reference for the returned values.
            :raises ProberException: if the command could not be executed successfully.
            :return: A tuple containing the x and y position in micrometer.
        """

        self.__comm.send("get_positioner_xy {0},{1}".format(probe.toSentioAbbr(), ref.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def get_probe_z(self, probe: ProbeSentio, ref: ProbeZReference) -> float:
        """ Get probe z position in micrometer.

            :param probe: The probe to get the position for.
            :param ref: The position reference for the returned values.
            :raises ProberException: if the command could not be executed successfully.
            :return: The z position in micrometer.
        """
        self.__comm.send("get_positioner_z {0}, {1}".format(probe.toSentioAbbr(), ref.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return float(resp.message())


    def move_probe_contact(self, probe: ProbeSentio) -> float:
        """ Move a probe to its contact position. 
        
            :param probe: The probe to move.
            :raises ProberException: if the command could not be executed successfully.
            :return: The z position after the move in micrometer (from zero).
        """

        self.__comm.send("move_positioner_contact {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        return float(resp.message())


    def move_probe_home(self, probe: ProbeSentio) -> Tuple[float, float]:
        """ Move probe to its home position.
         
            :param probe: The probe to move.
            :raises ProberException: if the command could not be executed successfully.
            :reteurn: A tuple containing the x and y position after the move.
        """

        self.__comm.send("move_positioner_home {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_probe_xy(self, probe: ProbeSentio, ref: ProbeXYReference, x: float, y: float) -> Tuple[float, float]:
        """ Move probe to a given position.
         
          :param probe: The probe to move.
          :param ref: The position reference for the submitted values.
          :param x: The x position in micrometer.
          :param y: The y position in micrometer.
          :raises ProberException: if the command could not be executed successfully.
          :return: A tuple containing the x and y position after the move.
        """

        self.__comm.send("move_positioner_xy {0},{1},{2},{3}".format(probe.toSentioAbbr(), ref.toSentioAbbr(), x, y))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])


    def move_probe_z(self, probe: ProbeSentio, ref: ProbeZReference, z: float) -> float:
        """ Move probe to a given z position. 

            :param probe: The probe to move.
            :param ref: The position reference for the submitted values.
            :param z: The target z position in micrometer.
            :raises ProberException: if the command could not be executed successfully.
            :return: The z position after the move in micrometer (from zero).
        """

        self.__comm.send("move_positioner_z {0}, {1}, {2}".format(probe.toSentioAbbr(), ref.toSentioAbbr(), z))
        resp = Response.check_resp(self.__comm.read_line())
        return float(resp.message())


    def set_probe_contact(self, probe: ProbeSentio, z: float = None) -> None:
        """ Set contact position of a positioner.
            
            :param probe: The probe to set contact height.
            :param z: The contact height in micrometer. If not specified, the current z position is used.
            :raises ProberException: if the command could not be executed successfully.
        """

        if z == None:
            self.__comm.send("set_positioner_contact {0}".format(probe.toSentioAbbr()))
        else:
            self.__comm.send("set_positioner_contact {0},{1}".format(probe.toSentioAbbr(), z))
        
        Response.check_resp(self.__comm.read_line())


    def set_probe_home(self, probe: ProbeSentio, site: ChuckSite = None, x: float = None, y: float = None) -> None:
        """ Set home position of a probe.
         
            :param probe: The probe to set home position.
            :param site: The chuck site to set the home position for. If None is specified the current site is used. 
            :param x: The x position in micrometer. If not specified, the current x position is used.
            :param y: The y position in micrometer. If not specified, the current y position is used.
            :raises ProberException: if the command could not be executed successfully.
        """
        if site == None:
            self.__comm.send("set_positioner_home {0}".format(probe.toSentioAbbr()))
        else:
            self.__comm.send(
                "set_positioner_home {0},{1},{2},{3}".format(probe.toSentioAbbr(), site.toSentioAbbr(), x, y))
            
        Response.check_resp(self.__comm.read_line())


    def step_probe_site(self, probe: ProbeSentio, idx: int ) -> Tuple[str, float, float]:
        """ Step to a specific probe site. 

            Each positioner can define n a number of predefined positions called "sites".
            This command initiates a step to such a site.
            
            :param probe: The probe to step.
            :param idx: The index of the site to step to.
            :raises ProberException: if the command could not be executed successfully.
            :return: A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """

        self.__comm.send("step_positioner_site {0},{1}".format(probe.toSentioAbbr(), idx))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])


    def step_probe_site_first(self, probe: ProbeSentio) -> Tuple[str, float, float]:
        """ Step to the first probe site.
         
            Each positioner can define n a number of predefined positions called "sites".
            This command initiates a step to the first site.

            :param probe: The probe to step.
            :raises ProberException: if the command could not be executed successfully.
            :return: A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """

        self.__comm.send("step_positioner_site_first {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])


    def step_probe_site_next(self, probe: ProbeSentio)  -> Tuple[str, float, float]:
        """ Step to the next probe site.
         
            Each positioner can define n a number of predefined positions called "sites".
            This command initiates a step to the next site.

            :param probe: The probe to step.
            :raises ProberException: if the command could not be executed successfully.
            :return: A tuple containing the site id, the x position in micrometer and the y position in micrometer.
        """
        
        self.__comm.send("step_positioner_site_next {0}".format(probe.toSentioAbbr()))
        resp = Response.check_resp(self.__comm.read_line())
        tok = resp.message().split(",")
        return tok[0], float(tok[1]), float(tok[2])
