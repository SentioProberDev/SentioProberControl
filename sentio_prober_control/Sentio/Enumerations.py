from enum import Enum
from deprecated import deprecated


@deprecated(reason="duplicated; CompensationMode instead.")
class Compensation(Enum):
    """ Represents a compensation type used by SENTIO. """

    Lateral = 0,
    """ Use lateral compensation """

    Vertical = 1,
    """ Use vertical compensation"""

    Both = 2,
    """ Use both lateral and vertical compensation. """

    ProbeCard = 3,
    """ Use probe card compensation. """

    MapScan = 4,
    """ Use map scan compensation. """

    Thermal = 5,
    """ Use thermal compensation. """

    Topography =6,
    """ Use Topography compensation. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            Compensation.Lateral: "lateral",
            Compensation.Vertical: "vertical",
            Compensation.Both: "both",
            Compensation.ProbeCard: "probecard",
            Compensation.MapScan: "mapscan",
            Compensation.Thermal: "thermal",
            Compensation.Topography: "topography"
        }
        return switcher.get(self, "Invalid compensation type")
    

class CompensationMode(Enum):
    """ Represents a compensation mode used by SENTIO. 
    
        The compensation mode is a selector that defines what principal type of compensation shall be used.
    """

    Lateral = 0,
    """ Use lateral compensation.
     
        The is an x,y copmensation performed based on the wafer and pre-trained patterns.  
    """

    Vertical = 1,
    """ Use vertical compensation. 
    
        Activate vertical compensation. Can be implemented with different means. (i.e. Topography)
    """

    Both = 2,
    """ Use both lateral and vertical compensation. 
    """

    ProbeCard = 3
    """ Use probe card compensation. 
    
        For true Probe-To-Pad-Alignment. Takes the position of the probe card into account.
        If you only use lateral compensation the wafer may be moved to the correct position
        but due to probe card drift the probes may not be in the correct position.
    """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            CompensationMode.Lateral: "Lateral",
            CompensationMode.Vertical: "Vertical",
            CompensationMode.Both: "Both",
            CompensationMode.ProbeCard: "ProbeCard"
        }
        return switcher.get(self, "Invalid CompensationMode")


class CompensationType(Enum):
    """ Compensation Type """
    
    DieAlign = 0,
    """ Die Alignment. 

        Use this for diced wafer with singulated dies on tape. 
    """

    Topography = 1,
    """ Topography scans the height og the wafer on chuck and created a height map.
    """

    MapScan = 2,
    """ MapScan scans the wafer once and created a x,y compensation table for later use. """

    AlignDie = 3,

    SkateDetection = 4
    """ Skate detection will use the visible skate of RF-probes to automatically determine the probe contact height. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            CompensationType.DieAlign: "DieAlign",
            CompensationType.Topography: "Topography",
            CompensationType.MapScan: "MapScan",
            CompensationType.AlignDie: "AlignDie",
            CompensationType.SkateDetection: "SkateDetection"
        }
        return switcher.get(self, "Invalid CompensationType")


class DefaultPattern(Enum):
    """ A list of slots for visual patterns used by SENTIO. 
    
        Each pattern is used for a specific purpose internally.
    """

    Align = 0,
    """ The pattern used for wafer alignment. """

    Home = 1,
    """ Pattern used for finding the home position"""

    DieAlignPos1 = 3,
    """ First pattern used for the die alignment. (on diced and taped wafers)"""
    
    DieAlignPos2 = 4,
    """ Second pattern used for the die alignment. (on diced and taped wafers)"""
    
    TwoPoint = 5,
    """ Pattern for Two-Point alignment"""
    
    Vce = 6,
    """ Pattern used for VCE contact height detection. """
    
    Ptpa = 7,
    """ A pattern used for probe to pad alignment. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            DefaultPattern.Align: "align",
            DefaultPattern.Home: "home",
            DefaultPattern.DieAlignPos1:   "diealignpos1",
            DefaultPattern.DieAlignPos2: "diealignpos2",
            DefaultPattern.TwoPoint: "2pt",
            DefaultPattern.Vce: "vce",
            DefaultPattern.Ptpa: "ptpa",
        }
        return switcher.get(self, "Invalid default pattern id")
    
    
@deprecated(reason="duplicated; Use CompensationMode instead.")
class OnTheFlyMode(Enum):
    Lateral = 0,
    Vertical = 1,
    Both =2,
    ProbeCard =3,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            OnTheFlyMode.Lateral: "AlignDie",
            OnTheFlyMode.Vertical: "MapScan",
            OnTheFlyMode.Both: "Topography",
            OnTheFlyMode.ProbeCard: "ProbeCard",
        }
        return switcher.get(self, "Invalid OTF mode")
    

class ProjectFileInfo(Enum):
    """ An enumerator containing the different aspects of retrieving current project info. """
    
    NameOnly = 0,
    """ Return only the project name. """
    
    FullPath = 1,
    """ Return the full path to the project file. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ProjectFileInfo.NameOnly: "Name",
            ProjectFileInfo.FullPath: "FullPath"
        }
        return switcher.get(self, "Invalid ProjectFileInfo")


class SteppingContactMode(Enum):
    """ This mode defines how the chuck behaves during steeping. """

    BackToContact = 0,
    """ Chuck will move back to contact position after stepping. """

    StepToSeparation = 1,
    """ Chuck will move to separation position after stepping. """
    
    LockContact = 2,
    """ Chuck cannot step when at contact. You will have to manually move it away from its contact position before issuing the next step command. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            SteppingContactMode.BackToContact: "BackToContact",
            SteppingContactMode.StepToSeparation: "StepToSeparation",
            SteppingContactMode.LockContact:   "LockContact"
        }
        return switcher.get(self, "Invalid stepping mode")


class Stage(Enum):
    """ Represents a stage in SENTIO.
     
        A stage is a piece of hardware that can be controlled by motors and moved in x, y and
        probably also z direction.  
    """
    Chuck = 0,
    """ The chuck stage. This is where the wafer is placed. """

    Scope = 1,
    """ The scope stage controls the downward looking microscope. This is an optional stage but it will be present on most probe stations. """

    Vce = 2,
    """ First Vce stage. Vce Stages can only be moved in z-direction."""

    Vce2 = 3,
    """ Second Vce stage. Vce Stages can only be moved in z-direction."""

    Probe1 = 4,
    """ First motorized probe. """

    Probe2 = 5,
    """ Second motorized probe. """

    Probe3 = 6,
    """ Third motorized probe. """

    Probe4 = 7
    """ Fourth motorized probe. """

    def toSentioAbbr(self):
        """ Convert the Stage enumerator into a string SENTIO understands. """
        switcher = {
            Stage.Chuck: "chuck",
            Stage.Scope: "scope",
            Stage.Vce:   "vce01",
            Stage.Vce2:  "vce02",            
            Stage.Probe1: "Probe01",
            Stage.Probe2: "Probe02",
            Stage.Probe3: "Probe03",
            Stage.Probe4: "Probe04"
        }
        return switcher.get(self, "Invalid stage")


class PoiReferenceXy(Enum):
    """ Referenc position for points of interest. 
    
        Each point of interest can either be defines with respect to the center of the stage.
        Or with respect to the center of the die.
    """

    DieCenter = 0,
    """ Use die center as the position reference. """

    StageCenter = 1
    """ Use stage center as the position reference. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """       
        switcher = {
            PoiReferenceXy.DieCenter: "DieCenter",
            PoiReferenceXy.StageCenter: "StageCenter"
        }
        return switcher.get(self, "Invalid stage")


class PtpaType(Enum):
    """ Defines the type of Probe to Pad Alignment used by SENTIO. """
    
    OffAxis = 0,
    """ Use off-axis PTPA with the platen camera and the chuck camera looking up to the probe tips. """

    OnAxis = 1,
    """ Use on axis PTPA with the scope camera looking down on the probe tips. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            PtpaType.OffAxis: "offaxis",
            PtpaType.OnAxis: "onaxis"
        }
        return switcher.get(self, "Invalid ptpa type")


class TestSelection(Enum):
    """ Specifies which dies shall be selected for test. 
    
        If a die is selected for test it is activated in the wafer map.
    """

    Nothing = 0,
    """ Select no dies. """

    Good = 1,
    """ Select only the good dies. 
    
        Good dies are the dies that are completely within the wafer map with no edge lying in the edge area of the map.
    """

    GoodAndUgly = 2,
    """ Select only the good dies. 
    
        Good dies are the dies that are completely within the wafer map with no edge lying in the edge area of the map.
        Ugly dies are the dies with at least one corner in the edge area of the map. The are completely present on the wafer
        but may be damaged or have incomplete structures.
    """

    GoodUglyAndEdge = 3,
    """ Good dies are the dies that are completely within the wafer map with no edge lying in the edge area of the map.
        Ugly dies are the dies with at least one corner in the edge area of the map. The are completely present on the wafer
        but may be damaged or have incomplete structures. The dies with at leas one edge outside of the wafer are called 
        edge dies. Those dies are incomplete.
     """

    All = 4
    """ Select all dies for testing even those that are completely outside of the wafer map. """


    def toSentioAbbr(self):
        """ Convert the TestSelection enumerator into a string SENTIO understands. """
        switcher = {
            TestSelection.Nothing: "n",
            TestSelection.Good: "g",
            TestSelection.GoodAndUgly: "u",
            TestSelection.GoodUglyAndEdge: "e",
            TestSelection.All: "a"
        }
        return switcher.get(self, "Invalid TestSelection")
    

class DetectionCoordindates(Enum):
    """ Specifies the coordinate system used for reporting box detections. 
    
        Used by SENTIO's built in DetectionAlgorithm
    """
    
    Image = 0,
    """ Use image coordinates. Results are returned as pixel coordinates. """

    Fov = 1,
    Roi = 2

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            DetectionCoordindates.Image: "Image",
            DetectionCoordindates.Fov: "Fov",
            DetectionCoordindates.Roi: "Roi"
        }
        return switcher.get(self, "Invalid DetectionCoordindates")


class DetectionAlgorithm(Enum):
    """ Specifes one of several of SENTIO's internal detection algorithms. 

        Not all versions of SENTIO support all algorithms. The most
        current versions of SENTIO have eliminated all models except
        for the ones based on deep learning.

        Those new Standard models detect multiple class of objects with 
        far greater reliability than the outdated models based on haar 
        cascades.
    """

    Keypoint = 0,            
    """ A Keypoint / ORB detector. """

    ProbeDetector = 1,
    """ Deep learning based AI model trained on various types of probe tips. 
    
        Detects different classes of probe tips with high reliability. Requires
        a pre-trained AI model in the sentio config folder (smod Extention)
    """

    WaferDetector = 2
    """ Deep learning based AI model trained on wafer structures. 

        Experimental detector for pads, street crossings, Text, Octagonal 
        Pads, RF structures and small dies.

        This is experimental functionality that may be removed or changed 
        at any time without prior warning!
    """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            DetectionAlgorithm.Keypoint: "Keypoint",
            DetectionAlgorithm.ProbeDetector: "ProbeDetector",
            DetectionAlgorithm.WaferDetector: "WaferDetector"
        }
        return switcher.get(self, "Invalid ProbeTipDetector")


class Module(Enum):
    """ An enumerator containing the names of all SENTIO modules.
    
        Module availability is determined by the specific type of probe station.
        All probe stations have the dashboard, setup and service modules. Most likely
        wafermap and Vision module will also be present (unless you have a purely manual 
        station)
    """

    Wafermap = 0,
    """ The wafermap module. """

    Vision = 1,
    """ The vision module"""

    Setup = 2,
    """ The setup module"""

    Service = 3,
    """ The service module"""

    Qalibria = 4,
    """The Qalibria module"""
    
    AuxSites = 5,
    """The aux site module"""

    Loader = 6,
    """The loader module"""
    
    Dashboard = 7
    """The dashboard module"""

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            Module.Wafermap: "Wafermap",
            Module.Vision: "Vision",
            Module.Setup: "Setup",
            Module.Service: "Service",
            Module.Qalibria: "Qalibria",
            Module.AuxSites: "AuxSites",
            Module.Loader: "Loader",
            Module.Dashboard: "Dashboard",
        }
        return switcher.get(self, "Invalid Module Name")


class AxisOrient(Enum):
    """ Represents an axis orientation. 

        Thie enumeration is mostly used to describe axis orientations
        on the computer screen. For instance the axis orientation
        of the wafer map.
    """
    
    DownRight = 0,
    """ Y axis pointing down; X axis pointing right. """

    DownLeft = 1,
    """ Y axis pointing down; X axis pointing left. """

    UpRight = 2,
    """ Y-axis pointing up; X axis pointing right. """

    UpLeft = 3
    """ Y-axis pointing up; X axis pointing left. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            AxisOrient.DownRight: "DR",
            AxisOrient.DownLeft: "DL",
            AxisOrient.UpRight: "UR",
            AxisOrient.UpLeft: "UL"
        }
        return switcher.get(self, "Invalid AxisOrient")


class DieNumber(Enum):
    """ Specifies how dies are numbered. """

    Present = 1,
    """ Number only dies that are present on the wafer. """

    Selected = 2
    """ Number only dies that are selected for test. """


class ColorScheme(Enum):
    """ The color scheme used by the wafer map.  """

    ColorFromBin = 0,
    """ The color of a die is determined by the bin code of the die. """

    ColorFromValue = 1
    """ The color of the die is determined by a floating point value attached to a die. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ColorScheme.ColorFromBin: 0,
            ColorScheme.ColorFromValue: 1
        }
        return switcher.get(self, "Invalid ColorScheme")

class OrientationMarker(Enum):
    """ Defines the wafers orientation marker. 
     
        Orientation markers can either be a notch or a flat in the wafer.  
        The orientation marker is used by the prealigner to detect
        the wafer position.

        Today mostly notches are used ar orientation markes as they reduce the 
        waste of wafer space.
    """
    
    Notch = 0,
    """ Wafer uses a notch. """

    Flat = 1
    """ Wafer uses a flat. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            OrientationMarker.Notch: "Notch",
            OrientationMarker.Flat: "Flat"
        }
        return switcher.get(self, "Invalid orientation marker")


class AutoFocusCmd(Enum):
    Calibration = 0,
    Focus = 1,
    GoTo = 2

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            AutoFocusCmd.Calibration: "C",
            AutoFocusCmd.Focus: "F",
            AutoFocusCmd.GoTo: "G"
        }
        return switcher.get(self, "Invalid auto focus function")


class AutoAlignCmd(Enum):
    AutoDieSize = 0,
    UpdateDieSize = 1,
    TwoPt = 2,
    CurrentDieSize = 3,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            AutoAlignCmd.AutoDieSize: "auto",
            AutoAlignCmd.UpdateDieSize: "update",
            AutoAlignCmd.TwoPt: "2pt",
            AutoAlignCmd.CurrentDieSize: ""
        }
        return switcher.get(self, "Invalid Auto Align function")


class ScopeXYReference(Enum):
    """ Position reference for scope motions. """
    
    Zero = 0,
    """ Use absolute scope coordinates. """

    Home = 1,
    """ Use coordinates with respect to the scope home position."""

    Relative = 2
    """ Use coordinates with respect to the current scope position."""

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ScopeXYReference.Zero: "Z",
            ScopeXYReference.Home: "H",
            ScopeXYReference.Relative: "R"
        }
        return switcher.get(self, "Invalid scope xy reference")


class ScopeZReference(Enum):
    """ Scope z reference for scoep motions. """

    Zero = 0,
    """ Move relative to the physical axis zero position. """

    Relative = 1
    """ Move relative to the current position. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ScopeZReference.Zero: "Z",
            ScopeZReference.Relative: "R"
        }
        return switcher.get(self, "Invalid scope z reference")


# Wishlist, not supported by Sentio right now!
class IMagProZReference(Enum):
    Zero = 0,
    Relative = 1,
    Center = 2

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            IMagProZReference.Zero: "Zero",
            IMagProZReference.Relative: "Relative",
            IMagProZReference.Center: "Center"
        }
        return switcher.get(self, "Invalid image pro z reference")


class AutoFocusAlgorithm(Enum):
    Gradient = 0,
    Bandpass = 1,
    Difference = 2,
    AutoCorrelation = 3

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            AutoFocusAlgorithm.Gradient: "Gradient",
            AutoFocusAlgorithm.Bandpass: "Bandpass",
            AutoFocusAlgorithm.Difference: "Difference",
            AutoFocusAlgorithm.AutoCorrelation: "AutoCorrelation"
        }
        return switcher.get(self, "Invalid focus measure")


class ChuckXYReference(Enum):
    """ Defines a reference for chuck xy motions. """

    Zero = 0,
    """ Use absolute chuck coordinates. """

    Home = 1,
    """ Use home position as reference. """

    Relative = 2,
    """ Use curent chuck position as reference. """

    Center = 3,
    """ Use chuck center position as reference. """

    User = 4,
    """ Use user defined coordinate system. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ChuckXYReference.Zero: "Z",
            ChuckXYReference.Home: "H",
            ChuckXYReference.Relative: "R",
            ChuckXYReference.Center: "C",
            ChuckXYReference.User: "U",
        }
        return switcher.get(self, "Invalid chuck xy reference")


class ChuckZReference(Enum):
    """ Defines a position reference for chuck z-motions."""

    Zero = 0,
    """ Use absolute chuck z coordinates with respect the the physical axis zero positon. """

    Relative = 1,
    """ Use relative chuck z coordinated with respect to the current position. """

    Contact = 2,
    """ Use relative chuck z coordinated with respect to the chucks contact height. """
    
    Hover = 3,
    """ Use relative chuck z coordinated with respect to the chucks hover height. """

    Separation = 4
    """ Use relative chuck z coordinated with respect to the chucks separation height. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ChuckZReference.Zero: "Z",
            ChuckZReference.Relative: "R",
            ChuckZReference.Contact: "C",
            ChuckZReference.Hover: "H",
            ChuckZReference.Separation: "S"
        }
        return switcher.get(self, "Invalid chuck z reference")


class ChuckThetaReference(Enum):
    """ Reference to use for chuck theat motions. """

    Zero = 0,
    """ Use zero of the theta axis."""

    Site = 1,
    """ Use the trained site of "home" angle as the reference. """

    Relative = 2
    """ Use the current theta position as reference. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ChuckThetaReference.Zero: "Z",
            ChuckThetaReference.Site: "S",
            ChuckThetaReference.Relative: "R"
        }
        return switcher.get(self, "Invalid chuck theta reference")


class WorkArea(Enum):
    """ An enumeration containing probe station work areas. """
    Probing = 0,
    """ The probing work are is the area in which the chuck is under the downward lookin microscope. This is where the wafer is probed. """
    
    Offaxis = 1,
    """ The off axis work area is the area in which the chuck is under the off axis camera. This is where off axis ptpa is performed. The wafer cannot be probed here because there is no probe card. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            WorkArea.Probing: "Probing",
            WorkArea.Offaxis: "Offaxis",
        }
        return switcher.get(self, "Invalid chuck site")


class ChuckSite(Enum):
    """ An enumeration containing chuck sites. 
    
        A chuck site is a physical position that is attached to the 
        chuck and is moving together with the chuck.
    """
    
    Wafer = 0,
    """ The wafer site. This is where your wafer is supposed to be. """

    AuxRight = 1,
    """ Right auxilliary site (if available)"""

    AuxLeft = 2,
    """ Left auxilliary site (if available)"""

    AuxRight2 = 3,
    """ Secondary right auxilliary site (if available)"""

    AuxLeft2 = 4,
    """ Secondary left auxilliary site (if available)"""

    ChuckCamera = 5,
    """ The chuck camera """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ChuckSite.Wafer: "Wafer",
            ChuckSite.AuxLeft: "AuxLeft",
            ChuckSite.AuxLeft2: "AuxLeft2",
            ChuckSite.AuxRight: "AuxRight",
            ChuckSite.AuxRight2: "AuxRight2",
            ChuckSite.ChuckCamera: "ChuckCamera",
        }
        return switcher.get(self, "Invalid chuck site")


class LoaderStation(Enum):
    """ An enumeration containing loader stations."""

    Cassette1 = 0,
    """ First cassette station. """

    Cassette2 = 1,
    """ Second cassette station."""

    PreAligner = 2,
    """ Prealigner Station for wafer prealignment. """
    
    Chuck = 3,
    """ The chuck station. """
    
    ForkA = 4,
    """ Robot fork A"""

    ForkB = 5,
    """ Roboit fork B"""

    WaferWallet = 6,
    """ 5 slow wafer wallet station"""

    IdReader = 7
    """ Id-reader station."""

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            LoaderStation.Cassette1: "cas1",
            LoaderStation.Cassette2: "cas2",
            LoaderStation.PreAligner: "pa",
            LoaderStation.Chuck: "chuck",
            LoaderStation.ForkA: "forka",
            LoaderStation.ForkB: "forkb",
            LoaderStation.WaferWallet: "ww"
        }
        return switcher.get(self, "Invalid loader station id")


class ProbeXYReference(Enum):
    Zero = 0,
    Home = 1,
    Relative = 2,
    Center = 3,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ProbeXYReference.Zero: "Z",
            ProbeXYReference.Home: "H",
            ProbeXYReference.Relative: "R",
            ProbeXYReference.Center: "C",
        }
        return switcher.get(self, "Invalid chuck xy reference")


class ProbeZReference(Enum):
    Zero = 0,
    Relative = 1,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ProbeZReference.Zero: "Z",
            ProbeZReference.Relative: "R",
        }
        return switcher.get(self, "Invalid chuck z reference")


class CameraMountPoint(Enum):
    """ Available camera mount points. 
    
        A camera mount point is a physical position in the prober where a camera can be located.
        SENTIO refers to its camera via the camera mount point.
    """

    Scope = 0,
    """ The downward looking microscope camera. """

    Scope2 = 1,
    """ Second scope camera. 
        This camera is only used by IMag to provide a wider field of view in addition to the scope camera.
    """

    Chuck = 2,
    """ The upward looking chuck camera. """

    OffAxis = 3,
    """ Downward looking platen camera."""

    Vce = 4,
    """ First Vce camera. """
    
    Vce2 = 5,
    """ Second Vce camera. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            CameraMountPoint.Scope: "scope",
            CameraMountPoint.Scope2: "scope2",
            CameraMountPoint.Chuck: "chuck",
            CameraMountPoint.OffAxis: "offaxis",
            CameraMountPoint.Vce: "vce01",
            CameraMountPoint.Vce2: "vce02"
        }
        return switcher.get(self, "Invalid camera mount point id")


class ChuckPositionHint(Enum):
    Center = 0,
    FrontLoad = 1,
    SideLoad = 2


class BinSelection(Enum):
    """ An enumerator for selecting dies for binning. """

    All = 0,
    """ Select dies and subsites. """

    DiesOnly = 1,
    """ Select dies only. """

    SubsitesOnly = 2
    """ Select subsites only.  """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            BinSelection.All: "a",
            BinSelection.DiesOnly: "d",
            BinSelection.SubsitesOnly: "s"
        }
        return switcher.get(self, "Invalid bin selection")


class RoutingPriority(Enum):
    """ Defines the stepping order """

    RowUniDir = 0,
    """ Rows first always step in same direction. """

    ColUniDir = 1,
    """ Columns first always step in same direction. """
    
    RowBiDir = 2,
    """ Rows first. Step odd rows backwards. """

    ColBiDir = 3
    """ Columns first. Step odd columns backwards. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
        """
        switcher = {
            RoutingPriority.RowUniDir: "r",
            RoutingPriority.ColUniDir: "c",
            RoutingPriority.RowBiDir: "wr",
            RoutingPriority.ColBiDir: "wc",
        }
        return switcher.get(self, "Invalid RoutingPriority enumerator")


class RoutingStartPoint(Enum):
    """ Defines the starting point for routing (stepping commands). """

    UpperLeft = 0,
    """ Stepping starts in upper left corner of the map. """

    UpperRight = 1,
    """ Stepping starts in upper right corner of the map. """

    LowerLeft = 2,
    """ Stepping stars in lower left corner of the map. """

    LowerRight = 3
    """ Stepping starts in lower right corner of the map. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
        """
        switcher = {
            RoutingStartPoint.UpperLeft: "ul",
            RoutingStartPoint.UpperRight: "ur",
            RoutingStartPoint.LowerLeft: "ll",
            RoutingStartPoint.LowerRight: "lr",
        }
        return switcher.get(self, "Invalid RoutingStartPoint enumerator")


class StatusBits:
    EndOfRoute = 1
    LastSite = 2


class RemoteCommandError:
        """ A list of possible error codes used by SENTIO.
        
            This list may not contain the full list of codes used by SENTIO due to 
            the fact that SENTIO is a moving target and new error codes may be added
            or removed.

            Have a look at the remote command specification to see which codes are
            supported by your version.
        """

        NoError = 0
        """ No error occured. """

        InternalError = 1
        """ An internal error occured in SENTIO. This is not supposed to happen and you can probably not fix the issue on your own. Please contact SENTIO support. """

        ExecutionError = 2
        """ A generic execution error. This is the most widely used error code to signal remote command failure. """

        CommandHandlerNotFound = 3
        """ A command handler for a certain subsystem of SENTIO was not found. This may happen when sending commands to a SENTIO module that is not 
            available on a given machine. """

        InvalidCommand = 4
        """ not used by SENTIO's native remote command set. """

        InvalidCommandFormat = 5
        """ not used by SENTIO's native remote command set. """

        InvalidParameter = 6
        """ A remote command parameter is incoreect.  """

        InvalidNumberOfParameters = 7
        """ The number of submitted remote command parameters is incoreect. """

        ArgumentOutOfBounds = 8
        """ A submitted parameter exceeds the range of allowed values. """

        FileNotFound = 9
        """ A file that was supposed to be loaded by SENTIO was not found. """

        InvalidFileFormat = 10
        """ not used by SENTIO's native remote command set. """
        
        EndOfRoute = 11
        """ Stepping reached the end of the route. """

        InvalidOperation = 12
        """ The requested operation is not allowed in the current state. """

        NotSupported = 13
        """ A function is not supported by a specific type of probe station. """

        SubsiteNotRoutable = 14
        """ The target of a stepping command is not marked for test and present. """

        ProjectRequired = 15
        """ A requested operation require an active project."""
        
        Unused = 16
        """ This error code is unused. """

        PrealignmentFailed = 17
        """ Prealignment failed. """

        HomePositionNotSet = 18
        """ The home position is not set."""

        Timeout = 19
        """ A command or operation timed out. """

        PatternNotTrained = 20
        """ A required pattern is not trained """

        PatternNotFound = 21
        """ A pattern could not be found """

        TooManyPatternsFound = 22
        """ Too many patterns were found """

        ContactHeightNotSet = 23
        """ The contact height is not set. """

        AutoFocusFailed = 24
        """ Auto focus failed on the wafer. """

        TipFocusFailed = 25
        """ Auto focus failed on the tips """

        TipNotFound = 26
        """  Cound not detect any tip on the probe card needle. """

        OffsetOverTolerance = 27
        """ The new Ptpa offset is gereter than tolerance z. """

        CommandPending = 30
        """ Returned when the status of an async command is polled with query_command_status and the command is Running """

        AsyncCommandAborted = 31
        """ Returned when a async command was aborted prematurely """

        UnknownCommandId = 32
        """ Returned when an async command is queried but SENTIO does not know anything about this command id """

        CameraNotCalibrated = 35
        """" A camera required for a vision task is not calibrated """

        CameraDoesNotExist = 36
        """ A required camera is not installed in the system. """

        AlignAccuracyBad = 37
        """ Alignment accuracy over 10 µm """

        SteppingWithWrongZPosition = 38
        """ Stepping when Chuck is below Separation """

        FrontDoorOpen = 60
        """ The front load door is open """

        LoaderDoorOpen = 61
        """ The side door is open """

        FrontDoorLockFail = 62
        """ Front door lock cannot be engaged """

        LoaderDoorLockFail = 63
        """ Side door lock cannot be engaged """

        SlotOrStationOccupied = 64
        """ A slot or station that is the target of a wafer transfer is already occupied """

        SlotOrStationEmpty = 65
        """ A slot or station that is the origin of a wafer transfer does not have a wafer """

        ProbeBackDoorOpen = 66
        """ The probe back door is open """

        ProbeSideDoorOpen = 67
        """  The probe side door is open (Not loader door, only TS2500/SE has this door, the door near the probe back door) """

        VacuumFailed = 68
        """ The vacuum failed """

        LoaderTrayDoorOpen = 69
        """ The tray door is open """

        LoaderCassetteDoesNotExist = 80
        LoaderSlotNumberError = 81
        LoaderPreAlignerAngleError = 83
        LoaderNoWaferOnPrealigner = 85
        LoaderNoWaferOnChuck = 86
        LoaderNoWaferAtSlotOrTray = 87
        LoaderNoWaferOnRobot = 88
        LoaderNoIdReader = 90
        LoaderReadIdFail = 91
        LoaderTransferWaferFail = 92
        LoaderNoWaferOnAuxiliary = 93

        ProbeNotInitialized = 100
        ProbeServoOnOffFail = 101

        OvertravelOutOfAxisLimit = 120
        MissingTopographyTable = 121
        IndexerDeviceIsNotExisting = 122

        LoaderWaferOnFork = 150
        LoaderWaferSlideOutCassette = 151
        LoaderNoWaferOnFork = 152
        LoaderWaferTrackerReceivedTimeout = 153
        LoaderWaferIsOblique = 154
        LoaderCassetteWithoutScan = 155
        LoaderPrealignerSensorSwitchSizeTimeOut = 156
        LoaderCassetteDoorBarOpenTimeout = 157
        LoaderCassetteDoorBarCloseTimeout = 158
        LoaderWaferIsCrossOver = 159
        LoaderWaferOnChuck = 160
        LoaderPrealignCalOffsetTooLarge = 161
        LoaderPrealignFailedTooMuchTime = 162
        LoaderConnectPrealignerFailed = 163
        LoaderWaferOnTray = 164
        LoaderCassetteMappingLagCountTooMuch = 165
        LoaderTransferSoakingTimeOut = 166
        LoaderUpdateMappingResultFail = 167
        LoaderTrayDoorLockTimeout = 168
        LoaderWaferOnPrealigner = 169

        ThermalSoakingTimeIsNotCorrect = 200

        SiPhMoveHoverFail = 300
        SiPhMoveSeparationFail = 301
        SiPhGradientSearchFail = 302
        SiPhFastAlignFail = 303
        SiPhPowerMeasurementFail = 304
        SiPhCouplingFail = 305
        SiPhTrackingFail = 306
        SiPhPivotPointSearchFail = 307

        PositionerSiteDataFail = 400

        QaChuckNotWorkingPosition = 450
        QaSubstrateNotSet = 451
        QaRemoteModeNotSet = 452
        QaStandardsEmpty = 453
        QaCalculateEtsFail = 454
        QaSetCalDriftDutDataFail = 455
        QaCalDriftDutNotFound = 456
        QaCalDriftDutFail = 457
        QaSwitchViewFail = 458
        QaExportCalDriftDataFail = 459


class FindPatternReference(Enum):
    DieHome = 0,
    CenterOfRoi = 1

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            FindPatternReference.DieHome: "DieHome",
            FindPatternReference.CenterOfRoi: "CenterOfRoi"
        }
        return switcher.get(self, "Invalid find pattern reference id")


class DialogButtons(Enum):
    """ A list of buttons that can be used in SENTIO's dialogs."""
    Ok = 1,
    """ An Ok button."""
    
    Yes = 2,
    """ A Yes button."""

    No = 3,
    """ A No button."""

    Cancel = 4,
    """ The Cancel button. """

    OkCancel = 5
    """ Both the Ok and the Cancel button. """

    YesNo = 6
    """ Both a Yes and a No button. """

    YesCancel = 7
    """ Yes and cancel button. """

    YesNoCancel = 8
    """ Yes, No and Cancel button. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            DialogButtons.Ok: "Ok",
            DialogButtons.Cancel: "Cancel",
            DialogButtons.OkCancel: "OkCancel",
            DialogButtons.Yes: "Yes",
            DialogButtons.No: "No",            
            DialogButtons.YesNo: "YesNo",
            DialogButtons.YesCancel: "YesCancel",
            DialogButtons.YesNoCancel: "YesNoCancel"                        
        }
        return switcher.get(self, "Invalid button id")


class LoadPosition(Enum):
    """ An enumeration containing the possible load positions.
     
        Not all load positions are available on all probe stations.
    """

    Front = 0,
    """ The Front Load position. All probe station have a front load position."""

    Side = 1
    """ The Side Load position. The side load position is optional and only present on systems with a side loader, a cassette loader or a wafer wallet. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            LoadPosition.Front: "front",
            LoadPosition.Side: "side"
        }
        return switcher.get(self, "Invalid Load position")


class VceZReference(Enum):
    """ Reference for Vce z motions. """

    Zero = 0,
    """ Move stage absolute. (relative to axis zero)"""

    Relative = 1
    """ Move stage relative to current position. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            VceZReference.Zero: "Z",
            VceZReference.Relative: "R"
        }
        return switcher.get(self, "Invalid vce z reference")


class SoftwareFence(Enum):
    Disabled = 0,
    Round = 1,
    Rectangle = 2,
    SoftwareLimit = 3

    def toSentioArg(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            SoftwareFence.Disabled: 'Disable',
            SoftwareFence.Rectangle: 'Rectangle',
            SoftwareFence.Round: 'Round',
            SoftwareFence.SoftwareLimit: 'SoftwareLimit',
        }
        return switcher.get(self, "Invalid SoftwareFence parameter")


class ImagePattern(Enum):
    align = 0,
    home = 1,
    diealignpos1 = 2,
    diealignpos2 =3,
    twoPt = 4,
    calc = 5

    def toSentioArg(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            ImagePattern.align: 'align',
            ImagePattern.home: 'home',
            ImagePattern.diealignpos1: 'diealignpos1',
            ImagePattern.diealignpos2: 'diealignpos2',
            ImagePattern.twoPt: '2pt',
            ImagePattern.calc: 'calc'
        }
        return switcher.get(self, "Invalid image pattern parameter")


class ProbeXYReference(Enum):
    Zero = 0,
    Home = 1,
    Current = 2,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            ProbeXYReference.Zero: "Zero",
            ProbeXYReference.Home: "Home",
            ProbeXYReference.Current: "Current",
        }
        return switcher.get(self, "Invalid probe xy reference")


class ProbeZReference(Enum):
    Zero = 0,
    Current = 1,
    Contact = 2,
    Separation = 3

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands.
            @private
        """
        switcher = {
            ProbeZReference.Zero: "Zero",
            ProbeZReference.Current: "Current",
            ProbeZReference.Contact: "Contact",
            ProbeZReference.Separation: "Separation"
        }
        return switcher.get(self, "Invalid probe z reference")


class ProbeSentio(Enum):
    East = 0,
    West = 1,
    North = 2,
    South = 3

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            ProbeSentio.East: "East",
            ProbeSentio.West: "West",
            ProbeSentio.North: "North",
            ProbeSentio.South: "South"
        }
        return switcher.get(self, "Invalid Probe reference")


class ExecuteCompensation(Enum):
    AlignDie = 0,
    MapScan = 1,
    Topography =2,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ExecuteCompensation.AlignDie: "AlignDie",
            ExecuteCompensation.MapScan: "MapScan",
            ExecuteCompensation.Topography: "Topography",
        }
        return switcher.get(self, "Invalid compensation type")



class ExecuteAction(Enum):
    """ Generic enumeration for execute actions. """

    Execute = 0,
    """ Execute the action. """

    Abort = 1,
    """ Abort an ongoing action. """

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            ExecuteAction.Execute: "execute",
            ExecuteAction.Abort: "abort",
        }
        return switcher.get(self, "Invalid ExecuteAction function")


class PtpaFindTipsMode(Enum):
    OnAxis = 0,
    OffAxis = 1,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. 
            @private
        """
        switcher = {
            PtpaFindTipsMode.OnAxis: "OnAxis",
            PtpaFindTipsMode.OffAxis: "OffAxis",
        }
        return switcher.get(self, "Invalid PTPA_Find_Tips_Mode function")


class DieCompensationType(Enum):
    DieAlign = 0,
    MapScan = 1,
    Topography = 2,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            DieCompensationType.DieAlign: "DieAlign",
            DieCompensationType.MapScan: "MapScan",
            DieCompensationType.Topography: "Topography",
        }
        return switcher.get(self, "Invalid Compensation_Type function")


class DieCompensationMode(Enum):
    Lateral = 0,
    Vertical = 1,
    Both = 2,
    ProbeCard = 3,
    SkateDetection = 4,

    def toSentioAbbr(self):
        """ Convert the enumerator into a string SENTIO understands. """
        switcher = {
            DieCompensationMode.Lateral: "Lateral",
            DieCompensationMode.Vertical: "Vertical",
            DieCompensationMode.Both: "Both",
            DieCompensationMode.ProbeCard: "ProbeCard",
            DieCompensationMode.SkateDetection: "SkateDetection",
        }
        return switcher.get(self, "Invalid DieCompensationMode function")


class ZPositionHint(Enum):
    """ Represents a hint for the z position of a stage. 
    
        Not all values are used by all stages. A scope does not have a contact height
        and a chuck Hover height may be disabled by SENTIO.
    """

    Default = 0,
    """ Used internally only. Essentially means the value is unset or undefined. """
    Contact = 1,
    """ Stage is at contact position. """
    Hover = 2,
    """ Stage is at hover position. """
    Separation = 3,
    """ Stage is at separation position """
    Lift = 4,
    """ Stage is at Lift position. """
    Transfer = 5
    """ Chuck is at transfer position. This is used for the chuck only when the loader is doing a wafer transfer internally. """

    def toSentioAbbr(self):
        """ Converts the enumerator into somthing a string SENTIO can understand. """
        switcher = {
            ZPositionHint.Default: "Default",
            ZPositionHint.Contact: "Contact",
            ZPositionHint.Hover: "Hover",
            ZPositionHint.Separation: "Separation",
            ZPositionHint.Lift: "Lift",
            ZPositionHint.Transfer: "Transfer",            
        }
        return switcher.get(self, "Invalid ZPositionHint")
