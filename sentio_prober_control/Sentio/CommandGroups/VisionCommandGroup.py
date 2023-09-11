from sentio_prober_control.Sentio.CommandGroups.CommandGroupBase import *
from sentio_prober_control.Sentio.CommandGroups.ModuleCommandGroupBase import ModuleCommandGroupBase
from sentio_prober_control.Sentio.CommandGroups.VisionCameraCommandGroup import VisionCameraCommandGroup
from sentio_prober_control.Sentio.CommandGroups.VisionIMagProCommandGroup import VisionIMagProCommandGroup
from sentio_prober_control.Sentio.CommandGroups.VisionCompensationGroup import VisionCompensationGroup
from sentio_prober_control.Sentio.Response import *
from sentio_prober_control.Sentio.Enumerations import *


class VisionCommandGroup(ModuleCommandGroupBase):
    """ A command group for accessing vision module functions."""

    def __init__(self, comm):
        """ Create a new instance of VisionCommandGroup.
            @private 
        """

        super().__init__(comm, 'vis')
        self.camera = VisionCameraCommandGroup(comm)
        """ A subgroup to provide logic for camera specific functions. """

        self.imagpro = VisionIMagProCommandGroup(comm)
        """ A subgroup to provide logic for IMagPro specific functions."""

        self.compensation = VisionCompensationGroup(comm)
        """ A subgroup to provide logic for compensation specific functions."""


    def align_wafer(self, mode: AutoAlignCmd) -> None:
        """ Perform a wafer alignment.

            :param mode: The alignment procedure to use. 
            :raises: ProberException if an error occured.
        """

        self._comm.send(f"vis:align_wafer {mode.toSentioAbbr()}")
        Response.check_resp(self._comm.read_line())


    def align_die(self, threshold: float = 0.05):
        """ Perform a die alignment. 
         
            Die alignment compensates for positional differences when working with diced wafers
            which contain single dies.

            :raises: ProberException if an error occured.
        """

        self._comm.send("vis:align_die {0}".format(threshold))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2])


    def auto_focus(self, af_cmd: AutoFocusCmd = AutoFocusCmd.Focus):
        """ Perform an auto focus operation.
        
            :param af_cmd: The auto focus command to execute.
            :raises: ProberException if an error occured.
            :return: The focus height in micrometer
        """

        self._comm.send("vis:auto_focus {0}".format(af_cmd.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(',')
        return float(tok[0])


    def camera_synchronize(self):
        self._comm.send("vis:camera_synchronize")
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2])


    def create_probepad_model(self, angleStep: float = 0.1, imgPath: str = None, UL:tuple=None, LR:tuple=None):  
        """ Creare probe pad model for NCC to matching pad from wafer. 
        
            Experimental functionality. DO NOT USE!

            if one parameter 
                create pad model from camera 
            else 
                create pad model from image file 

            @private
        """
        if imgPath==None:
            self._comm.send("vis:create_probepad_model {0}".format(angleStep))
        else:            
            self._comm.send("vis:create_probepad_model {0},{1},{2},{3},{4},{5}".format(angleStep,imgPath, UL[0],  UL[1], LR[0], LR[1]))

        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        print(resp)
        return tok 
    

    def detect_probepads(self, imgPath: str = None, minScore:float=0.7, startAngle:float=None, startExtend:float=None,maxOverlap:float=None): 
        """ Execute pad pattern match with NCC. 

            This command is not for public consumption! DO NOT USE IT!
        
            @private
        """  

        if startAngle==None:
            self._comm.send("vis:detect_probepads {},{}".format(imgPath, minScore))
        else:            
            self._comm.send("vis:detect_probepads {},{},{},{},{}".format(imgPath, minScore, startAngle,  startExtend, maxOverlap))

        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return bool(tok[0]), float(tok[1]), tok[2]


    def detect_probetips(self, camera: CameraMountPoint, detector:  DetectionAlgorithm = DetectionAlgorithm.ProbeDetector, coords: DetectionCoordindates = DetectionCoordindates.Roi):
        """ Executes a built in detector on a given camera and return a list of detection results.

            :param camera: The camera to use for detection.
            :param detector: The detection algorithm to use.
            :param coords: The coordinates to use for the returned detection results.
            :raises: ProberException if an error occured.
            :return: A list of detected tips. Each detection result is a tuply of 6 values: x, y, width, height, score, class_id.
        """        

        self._comm.send("vis:detect_probetips {0}, {1}, {2}".format(camera.toSentioAbbr(), detector.toSentioAbbr(), coords.toSentioAbbr(), coords.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        str_tips = resp.message().split(",")

        found_tips = []
        cid = 0
        for n in range(0, len(str_tips)):
            str_tip = str_tips[n].strip().split(" ")
            num_col = len(str_tip)

            x = float(str_tip[0])    # tip x position
            y = float(str_tip[1])    # tip y position
            w = float(str_tip[2])    # detection width
            h = float(str_tip[3])    # detection height
            q = float(str_tip[4])    # detection quality (meaning depends on the used detector)
            
            if num_col>=6:
                cid = float(str_tip[5])  # class id (only multi class detectors)

            found_tips.append([x, y, w, h, q, cid])

        return found_tips


    def enable_follow_mode(self, stat:bool) -> None:
        """ Enable or disable the scope follow mode.

            If scope follow mode is active the scope will move in sync with the chuck. This is useful for
            keeping the image in focus while moving the chuck.

            This function wraps the "vis:enable_follow_mode" remote command.

            :param stat: A flag indicating whether to enable or disable the follow mode.
            :raises: ProberException if an error occured.
        """
        self._comm.send("vis:enable_follow_mode {0}".format(stat))
        Response.check_resp(self._comm.read_line())


    def find_home(self) -> None:
        """ Find home position.
         
            This function uses a pre-trained pattern to fully automatically find the home position.

            :raises: ProberException if an error occured.  
        """

        self._comm.send("vis:find_home")
        Response.check_resp(self._comm.read_line())


    def find_pattern(self, name: str, threshold: float = 70, pattern_index: int = 0, reference: FindPatternReference = FindPatternReference.CenterOfRoi, can_fail_detection: bool = False):
        """ Find a trained pattern in the camera image. 
        
            :param name: The name of the pattern to find.
            :param threshold: The detection threshold. The higher the threshold, the more certain the detection must be.
            :param pattern_index: The index of the pattern to find. In SENTIO each pattern may have up to 5 alternate patterns. This is the index of the alternate pattern.
            :param reference: The reference point to use for the pattern detection.
            :param can_fail_detection: 
        """
        self._comm.send("vis:find_pattern {0}, {1}, {2}, {3}".format(name, threshold, pattern_index, reference.toSentioAbbr()))
        if can_fail_detection == False:
            resp = Response.check_resp(self._comm.read_line())
            tok = resp.message().split(",")
            return float(tok[0]), float(tok[1]), float(tok[2]), float(tok[3])
        else:
            try:
                resp = Response.check_resp_allow_error(self._comm.read_line())
                ret = resp.errc()
                return float(ret), resp.message()
            except Exception as e:
                print(str(e))


    def has_camera(self, camera: CameraMountPoint) -> bool:
        """ Check wether a given camera is present in the system.
         
            This function wraps the "vis:has_camera" remote command.

            :param camera: The camera mount point to check.
            :raises: ProberException if an error occured.
            :return: True if the camera is present, False otherwise.  
        """

        self._comm.send(f"vis:has_camera {camera.toSentioAbbr()}")
        resp = Response.check_resp(self._comm.read_line())
        return resp.message().upper()=="1"


    def switch_all_lights(self, stat:bool):
        """ Switch all camera lights on or off. 
            
            This function wraps the "vis:switch_all_lights" remote command.    
        
            :param stat: A flag indicating whether to switch the lights on or off.
            :raises: ProberException if an error occured.
        """

        self._comm.send("vis:switch_all_lights {0}".format(stat))
        Response.check_resp(self._comm.read_line())


    def remove_probetip_marker(self):
        """ Remove probetip marker from the camera display.
            :raises: ProberException if an error occured.
        """
        self._comm.send("vis:remove_probetip_marker")
        Response.check_resp(self._comm.read_line())

    
    def match_tips(self, ptpa_type:PtpaType):
        """ For internal use only!
            This function is subject to change without any prior warning. MPI will not maintain backwards 
            compatibility or provide support. """        

        self._comm.send("vis:match_tips {0}".format(ptpa_type.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1])

    def snap_image(self, file: str):
        self._comm.send("vis:snap_image {0}".format(file))
        Response.check_resp(self._comm.read_line())

    def switch_light(self, camera: CameraMountPoint, stat: bool):
        self._comm.send("vis:switch_light {0}, {1}".format(camera.toSentioAbbr(), stat))
        Response.check_resp(self._comm.read_line())

    def switch_camera(self, camera: CameraMountPoint):
        self._comm.send("vis:switch_camera {0}".format(camera.toSentioAbbr()))
        Response.check_resp(self._comm.read_line())


    def ptpa_find_pads(self, row: int = 0, column: int = 0):
        self._comm.send("vis:execute_ptpa_find_pads {0},{1}".format(row, column))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2])

    def ptpa_find_tips(self, ptpa_mode: PtpaFindTipsMode):
        self._comm.send("vis:ptpa_find_tips {0}".format(ptpa_mode.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())
        tok = resp.message().split(",")
        return float(tok[0]), float(tok[1]), float(tok[2])

    def start_execute_compensation(self, comp_type: DieCompensationType, comp_mode: DieCompensationMode):
        self._comm.send("vis:compensation:start_execute {0},{1}".format(comp_type.toSentioAbbr(), comp_mode.toSentioAbbr()))
        resp = Response.check_resp(self._comm.read_line())

        if not resp.ok():
            raise ProberException(resp.message())

        return resp.cmd_id()