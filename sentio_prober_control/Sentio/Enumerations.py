from enum import Enum

from deprecated import deprecated


class AutoAlignCmd(Enum):
    """Specifies an algorithm for performaing auto alignment.

    Attributes:
        AutoDieSize (0): Perform auto alignment. Determine die size with zero prior knowledge.
        UpdateDieSize (1): Perform auto alignment. Update die size based on current value.
        TwoPt (2): Use Two-Point alignment algorithm.
    """

    AutoDieSize = 0
    UpdateDieSize = 1
    TwoPt = 2

    def toSentioAbbr(self):
        switcher = {
            AutoAlignCmd.AutoDieSize: "auto",
            AutoAlignCmd.UpdateDieSize: "update",
            AutoAlignCmd.TwoPt: "2pt",
        }
        return switcher.get(self, "Invalid Auto Align function")


class AutoFocusAlgorithm(Enum):
    """A list of different AutoFocus algorithms.

    Attributes:
        Gradient (0): Gradient Engery
        Bandpass (1): Bandpass Filter
        Difference (2): Difference
        AutoCorrelation (3): Auto Correlation
    """

    Gradient = 0
    Bandpass = 1
    Difference = 2
    AutoCorrelation = 3

    def toSentioAbbr(self):
        switcher = {
            AutoFocusAlgorithm.Gradient: "Gradient",
            AutoFocusAlgorithm.Bandpass: "Bandpass",
            AutoFocusAlgorithm.Difference: "Difference",
            AutoFocusAlgorithm.AutoCorrelation: "AutoCorrelation",
        }
        return switcher.get(self, "Invalid focus measure")


class AutoFocusCmd(Enum):
    """A list of different AutoFocus functions.

    Attributes:
        Calibration (0): Execute focus calibration.
        Focus (1): Measure Focus curve and determine maximum.
        GoTo (2): Simply move the scope to distance from the wafer that is known to be in focus.
    """

    Calibration = 0
    Focus = 1
    GoTo = 2

    def toSentioAbbr(self):
        switcher = {
            AutoFocusCmd.Calibration: "C",
            AutoFocusCmd.Focus: "F",
            AutoFocusCmd.GoTo: "G",
        }
        return switcher.get(self, "Invalid auto focus function")


class AxisOrient(Enum):
    """Represents an axis orientation.

    Thie enumeration is mostly used to describe axis orientations
    on the computer screen. For instance the axis orientation
    of the wafer map.

    Attributes:
        DownRight (0): Y axis pointing down; X axis pointing right.
        DownLeft (1): Y axis pointing down; X axis pointing left.
        UpRight (2): Y-axis pointing up; X axis pointing right.
        UpLeft (3): Y-axis pointing up; X axis pointing left.
    """

    DownRight = 0
    DownLeft = 1
    UpRight = 2
    UpLeft = 3

    def toSentioAbbr(self):
        switcher = {
            AxisOrient.DownRight: "DR",
            AxisOrient.DownLeft: "DL",
            AxisOrient.UpRight: "UR",
            AxisOrient.UpLeft: "UL",
        }
        return switcher.get(self, "Invalid AxisOrient")


class BinSelection(Enum):
    """An enumerator for selecting dies for binning.

    Attributes:
        All (0): Select dies and subsites.
        DiesOnly (1): Select dies only.
        SubsitesOnly (2): Select subsites only.
    """

    All = 0
    DiesOnly = 1
    SubsitesOnly = 2

    def toSentioAbbr(self):
        switcher = {
            BinSelection.All: "a",
            BinSelection.DiesOnly: "d",
            BinSelection.SubsitesOnly: "s",
        }
        return switcher.get(self, "Invalid bin selection")


class BinQuality(Enum):
    """An enumerator dor defining the quality parameter of a certain bin code.

    Attributes:
        All (0): Select dies and subsites.
        DiesOnly (1): Select dies only.
        SubsitesOnly (2): Select subsites only.
    """

    Pass = 0
    Fail = 1
    Undefined = 2

    def toSentioAbbr(self):
        switcher = {
            BinQuality.Pass: 0,
            BinQuality.Fail: 1,
            BinQuality.Undefined: 2,
        }
        return switcher.get(self, "Invalid bin quality identifier")


class CameraMountPoint(Enum):
    """Available camera mount points.

    A camera mount point is a physical position in the prober where a camera can be located.
    SENTIO refers to its camera via the camera mount point.

    Attributes:
        Scope (0): The downward looking microscope camera.
        Scope2 (1): Second scope camera. This camera is only used by IMag to provide a wider field of view in addition to the scope camera.
        Chuck (2): The upward looking chuck camera.
        OffAxis (3): Downward looking platen camera.
        Vce (4): First Vce camera.
        Vce2 (5): Second Vce camera.
    """

    Scope = 0
    Scope2 = 1
    Chuck = 2
    OffAxis = 3
    Vce = 4
    Vce2 = 5

    def toSentioAbbr(self):
        switcher = {
            CameraMountPoint.Scope: "scope",
            CameraMountPoint.Scope2: "scope2",
            CameraMountPoint.Chuck: "chuck",
            CameraMountPoint.OffAxis: "offaxis",
            CameraMountPoint.Vce: "vce01",
            CameraMountPoint.Vce2: "vce02",
        }
        return switcher.get(self, "Invalid camera mount point id")


class ChuckPositionHint(Enum):
    """Position hint for the chuck stage.

    Attributes:
        Center (0): Chuck is at Center Position
        FrontLoad (1): Chuck is at Front Load Position
        SideLoad (2): Chuck is at Side Load Position
    """

    Center = 0
    FrontLoad = 1
    SideLoad = 2


class ChuckSite(Enum):
    """An enumeration containing chuck sites.

    A chuck site is a physical position that is attached to the
    chuck and is moving together with the chuck.

    Attributes:
        Wafer (0): The wafer site. This is where your wafer is supposed to be.
        AuxRight (1): Right auxilliary site (if available)
        AuxLeft (2): Left auxilliary site (if available)
        AuxRight2 (3): Secondary right auxilliary site (if available)
        AuxLeft2 (4): Secondary left auxilliary site (if available)
        ChuckCamera (5): The chuck camera
    """

    Wafer = 0
    AuxRight = 1
    AuxLeft = 2
    AuxRight2 = 3
    AuxLeft2 = 4
    ChuckCamera = 5

    def toSentioAbbr(self):
        switcher = {
            ChuckSite.Wafer: "Wafer",
            ChuckSite.AuxLeft: "AuxLeft",
            ChuckSite.AuxLeft2: "AuxLeft2",
            ChuckSite.AuxRight: "AuxRight",
            ChuckSite.AuxRight2: "AuxRight2",
            ChuckSite.ChuckCamera: "ChuckCamera",
        }
        return switcher.get(self, "Invalid chuck site")


class ChuckThetaReference(Enum):
    """Reference to use for chuck theat motions.

    Attributes:
        Zero (0): Use zero of the theta axis.
        Site (1): Use the trained site of "home" angle as the reference.
        Relative (2): Use the current theta position as reference.
    """

    Zero = 0
    Site = 1
    Relative = 2

    def toSentioAbbr(self):
        switcher = {
            ChuckThetaReference.Zero: "Z",
            ChuckThetaReference.Site: "S",
            ChuckThetaReference.Relative: "R",
        }
        return switcher.get(self, "Invalid chuck theta reference")


class ChuckXYReference(Enum):
    """Defines a reference for chuck xy motions.

    Attributes:
        Zero (0): Use absolute chuck coordinates.
        Home (1): Use home position as reference.
        Relative (2): Use curent chuck position as reference.
        Center (3): Use chuck center position as reference.
        User (4): Use user defined coordinate system.
    """

    Zero = 0
    Home = 1
    Relative = 2
    Center = 3
    User = 4

    def toSentioAbbr(self):
        switcher = {
            ChuckXYReference.Zero: "Z",
            ChuckXYReference.Home: "H",
            ChuckXYReference.Relative: "R",
            ChuckXYReference.Center: "C",
            ChuckXYReference.User: "U",
        }
        return switcher.get(self, "Invalid chuck xy reference")


class ChuckZReference(Enum):
    """Defines a position reference for chuck z-motions.

    Attributes:
        Zero (0): Use absolute chuck z coordinates with respect the the physical axis zero positon.
        Relative (1): Use relative chuck z coordinated with respect to the current position.
        Contact (2): Use relative chuck z coordinated with respect to the chucks contact height.
        Hover (3): Use relative chuck z coordinated with respect to the chucks hover height.
        Separation (4): Use relative chuck z coordinated with respect to the chucks separation height.
    """

    Zero = 0
    Relative = 1
    Contact = 2
    Hover = 3
    Separation = 4

    def toSentioAbbr(self):
        switcher = {
            ChuckZReference.Zero: "Z",
            ChuckZReference.Relative: "R",
            ChuckZReference.Contact: "C",
            ChuckZReference.Hover: "H",
            ChuckZReference.Separation: "S",
        }
        return switcher.get(self, "Invalid chuck z reference")


class ColorScheme(Enum):
    """The color scheme used by the wafer map.

    Attributes:
        ColorFromBin (0): The color of a die is determined by the bin code of the die.
        ColorFromValue (1): The color of the die is determined by a floating point value attached to a die.
    """

    ColorFromBin = 0
    ColorFromValue = 1

    def toSentioAbbr(self):
        switcher = {ColorScheme.ColorFromBin: 0, ColorScheme.ColorFromValue: 1}
        return switcher.get(self, "Invalid ColorScheme")


@deprecated(reason="duplicated; use DieCompensationMode instead.")
class Compensation(Enum):
    Lateral = 0
    Vertical = 1
    Both = 2
    ProbeCard = 3
    MapScan = 4
    Thermal = 5
    Topography = 6

    def toSentioAbbr(self):
        switcher = {
            Compensation.Lateral: "lateral",
            Compensation.Vertical: "vertical",
            Compensation.Both: "both",
            Compensation.ProbeCard: "probecard",
            Compensation.MapScan: "mapscan",
            Compensation.Thermal: "thermal",
            Compensation.Topography: "topography",
        }
        return switcher.get(self, "Invalid compensation type")


class CompensationMode(Enum):
    """A list with available compensation modes.

    Attributes:
        Lateral (0): Lateral (XY) compensation.
        Vertical (1): Vertical (Z) compensation.
        Both (2): Both lateral and vertical compensation.
        ProbeCard (3): Probe card compensation.
        MapScan (4): MapScan compensation.
        Topography (5): Topography compensation.
    """

    Lateral = 0
    Vertical = 1
    Both = 2
    ProbeCard = 3
    MapScan = 4
    Thermal = 5
    Topography = 6

    def toSentioAbbr(self):
        switcher = {
            CompensationMode.Lateral: "Lateral",
            CompensationMode.Vertical: "Vertical",
            CompensationMode.Both: "Both",
            CompensationMode.ProbeCard: "ProbeCard",
            CompensationMode.MapScan: "mapscan",
            CompensationMode.Thermal: "thermal",
            CompensationMode.Topography: "topography",
        }
        return switcher.get(self, "Invalid CompensationMode")


class CompensationType(Enum):
    """A list of compensation types.

    Attributes:
        DieAlign (0):
        Topography (1): Vertical (Z) compensation.
        MapScan (2): Both lateral and vertical compensation.
        AlignDie (3): Probe card compensation.
        SkateDetection (4): MapScan compensation.
    """

    DieAlign = 0
    Topography = 1
    MapScan = 2
    AlignDie = 3
    SkateDetection = 4
    OnTheFly = 5
    OffAxis = 6

    def toSentioAbbr(self):
        switcher = {
            CompensationType.DieAlign: "DieAlign",
            CompensationType.Topography: "Topography",
            CompensationType.MapScan: "MapScan",
            CompensationType.AlignDie: "AlignDie",
            CompensationType.SkateDetection: "SkateDetection",
            CompensationType.OnTheFly: "OnTheFly",
            CompensationType.OffAxis: "OffAxis",
        }
        return switcher.get(self, "Invalid CompensationType")


class DefaultPattern(Enum):
    """A list of slots for visual patterns used by SENTIO.

    Each pattern is used for a specific purpose internally.

    Attributes:
        Align (0): The pattern used for wafer alignment.
        Home (1): Pattern used for finding the home position
        DieAlignPos1 (3): First pattern used for the die alignment. (on diced and taped wafers)
        DieAlignPos2 (4): Second pattern used for the die alignment. (on diced and taped wafers)
        TwoPoint (5): Pattern for Two-Point alignment
        Vce (6): Pattern used for VCE contact height detection.
        Ptpa (7): A pattern used for probe to pad alignment.
    """

    Align = 0
    Home = 1
    DieAlignPos1 = 3
    DieAlignPos2 = 4
    TwoPoint = 5
    Vce = 6
    Ptpa = 7

    def toSentioAbbr(self):
        switcher = {
            DefaultPattern.Align: "align",
            DefaultPattern.Home: "home",
            DefaultPattern.DieAlignPos1: "diealignpos1",
            DefaultPattern.DieAlignPos2: "diealignpos2",
            DefaultPattern.TwoPoint: "2pt",
            DefaultPattern.Vce: "vce",
            DefaultPattern.Ptpa: "ptpa",
        }
        return switcher.get(self, "Invalid default pattern id")


class DetectionAlgorithm(Enum):
    """Specifes one of several of SENTIO's internal detection algorithms.

    Not all versions of SENTIO support all algorithms. The most
    current versions of SENTIO have eliminated all models except
    for the ones based on deep learning.

    Those new Standard models detect multiple class of objects with
    far greater reliability than the outdated models based on haar
    cascades.

    Attributes:
        Keypoint (0): A Keypoint / ORB detector.
        ProbeDetector (1): Deep learning based AI model trained on various types of probe tips.
        WaferDetector (2): Deep learning based AI model trained on wafer structures.
    """

    Keypoint = 0
    ProbeDetector = 1
    WaferDetector = 2

    def toSentioAbbr(self):
        switcher = {
            DetectionAlgorithm.Keypoint: "Keypoint",
            DetectionAlgorithm.ProbeDetector: "ProbeDetector",
            DetectionAlgorithm.WaferDetector: "WaferDetector",
        }
        return switcher.get(self, "Invalid ProbeTipDetector")


class DetectionCoordindates(Enum):
    """Specifies the coordinate system used for reporting box detections.

    Used by SENTIO's built in DetectionAlgorithm

    Attributes:
        Image (0): Use image coordinates. Results are returned as pixel coordinates.
        Fov (1): Coordinates are in micrometer relative to the center of the field of view.
        Roi (2): Coordinates are in micrometer relative to the center of the region of interest.
    """

    Image = 0
    Fov = 1
    Roi = 2

    def toSentioAbbr(self):
        switcher = {
            DetectionCoordindates.Image: "Image",
            DetectionCoordindates.Fov: "Fov",
            DetectionCoordindates.Roi: "Roi",
        }
        return switcher.get(self, "Invalid DetectionCoordindates")


class DialogButtons(Enum):
    """A list of buttons that can be used in SENTIO's dialogs.

    Attributes:
        Ok (1): An Ok button.
        Yes (2): A Yes button.
        No (3): A No button.
        Cancel (4): A Cancel button.
        OkCancel (5): Both the Ok and the Cancel button.
        YesNo (6): Both a Yes and a No button.
        YesCancel (7): Yes and cancel button.
        YesNoCancel (8): Yes, No and Cancel button.
    """

    Ok = 1
    Yes = 2
    No = 3
    Cancel = 4
    OkCancel = 5
    YesNo = 6
    YesCancel = 7
    YesNoCancel = 8

    def toSentioAbbr(self):
        switcher = {
            DialogButtons.Ok: "Ok",
            DialogButtons.Cancel: "Cancel",
            DialogButtons.OkCancel: "OkCancel",
            DialogButtons.Yes: "Yes",
            DialogButtons.No: "No",
            DialogButtons.YesNo: "YesNo",
            DialogButtons.YesCancel: "YesCancel",
            DialogButtons.YesNoCancel: "YesNoCancel",
        }
        return switcher.get(self, "Invalid button id")


@deprecated("Use CompensationMode instead")
class DieCompensationMode(Enum):
    """Represents a compensation mode used by SENTIO.

    The compensation mode is a selector that defines what principal type of compensation shall be used.

    Attributes:
        Lateral (0): Use lateral compensation.
        Vertical (1): Use vertical compensation.
        Both (2): Use both lateral and vertical compensation.
        ProbeCard (3): Use probe card compensation.
        SkateDetection (4): Use skate detection
    """

    Lateral = 0
    Vertical = 1
    Both = 2
    ProbeCard = 3
    SkateDetection = 4

    def toSentioAbbr(self):
        switcher = {
            DieCompensationMode.Lateral: "Lateral",
            DieCompensationMode.Vertical: "Vertical",
            DieCompensationMode.Both: "Both",
            DieCompensationMode.ProbeCard: "ProbeCard",
            DieCompensationMode.SkateDetection: "SkateDetection",
        }
        return switcher.get(self, "Invalid DieCompensationMode function")


class DieCompensationType(Enum):
    """Compensation Type.

    Attributes:
        DieAlign (0): Die Alignment.
        MapScan (1): MapScan scans the wafer once and created a x,y compensation table for later use.
        Topography (2): Topography scans the height og the wafer on chuck and created a height map.
    """

    DieAlign = 0
    MapScan = 1
    Topography = 2

    def toSentioAbbr(self):
        switcher = {
            DieCompensationType.DieAlign: "DieAlign",
            DieCompensationType.MapScan: "MapScan",
            DieCompensationType.Topography: "Topography",
        }
        return switcher.get(self, "Invalid Compensation_Type function")


class DieNumber(Enum):
    """Specifies how dies are numbered.

    Attributes:
        Present (1): Number only dies that are present on the wafer.
        Selected (2): Number only dies that are selected for test.
    """

    Present = 1
    Selected = 2


@deprecated("ExecuteAction is deprecated.")
class ExecuteAction(Enum):
    Execute = 0
    Abort = 1

    def toSentioAbbr(self):
        switcher = {
            ExecuteAction.Execute: "execute",
            ExecuteAction.Abort: "abort",
        }
        return switcher.get(self, "Invalid ExecuteAction function")


@deprecated("ExecuteCompensation is deprecated.")
class ExecuteCompensation(Enum):
    AlignDie = 0
    MapScan = 1
    Topography = 2

    def toSentioAbbr(self):
        switcher = {
            ExecuteCompensation.AlignDie: "AlignDie",
            ExecuteCompensation.MapScan: "MapScan",
            ExecuteCompensation.Topography: "Topography",
        }
        return switcher.get(self, "Invalid compensation type")


class FindPatternReference(Enum):
    """Reference point for coordinates than returning a pattern position.

    Attributes:
        DieHome (0): Use Die Home position as reference.
        CenterOfRoi (1): Use Center of ROI as reference.
    """

    DieHome = 0
    CenterOfRoi = 1

    def toSentioAbbr(self):
        switcher = {
            FindPatternReference.DieHome: "DieHome",
            FindPatternReference.CenterOfRoi: "CenterOfRoi",
        }
        return switcher.get(self, "Invalid find pattern reference id")


class ImagePattern(Enum):
    align = 0
    home = 1
    diealignpos1 = 2
    diealignpos2 = 3
    twoPt = 4
    calc = 5

    def toSentioArg(self):
        switcher = {
            ImagePattern.align: "align",
            ImagePattern.home: "home",
            ImagePattern.diealignpos1: "diealignpos1",
            ImagePattern.diealignpos2: "diealignpos2",
            ImagePattern.twoPt: "2pt",
            ImagePattern.calc: "calc",
        }
        return switcher.get(self, "Invalid image pattern parameter")


class IMagProZReference(Enum):
    Zero = 0
    Relative = 1
    Center = 2

    def toSentioAbbr(self):
        switcher = {
            IMagProZReference.Zero: "Zero",
            IMagProZReference.Relative: "Relative",
            IMagProZReference.Center: "Center",
        }
        return switcher.get(self, "Invalid image pro z reference")


class LoaderStation(Enum):
    """An enumeration containing loader stations.

    Attributes:
        Cassette1 (0): First cassette station.
        Cassette2 (1): Second cassette station.
        PreAligner (2): Prealigner Station for wafer prealignment.
        Chuck (3): The chuck station.
        ForkA (4): Robot fork A
        ForkB (5): Roboit fork B
        WaferWallet (6): 5 slow wafer wallet station
        IdReader (7): Id-reader station.
    """

    Cassette1 = 0
    Cassette2 = 1
    PreAligner = 2
    Chuck = 3
    ForkA = 4
    ForkB = 5
    WaferWallet = 6
    IdReader = 7

    def toSentioAbbr(self):
        switcher = {
            LoaderStation.Cassette1: "cas1",
            LoaderStation.Cassette2: "cas2",
            LoaderStation.PreAligner: "pa",
            LoaderStation.Chuck: "chuck",
            LoaderStation.ForkA: "forka",
            LoaderStation.ForkB: "forkb",
            LoaderStation.WaferWallet: "ww",
        }
        return switcher.get(self, "Invalid loader station id")


class LoadPosition(Enum):
    """An enumeration containing the possible load positions.

    Not all load positions are available on all probe stations.

    Attributes:
        Front (0): The Front Load position. All probe station have a front load position.
        Side (1): The Side Load position. The side load position is optional and only present on systems with a side loader, a cassette loader or a wafer wallet.
    """

    Front = 0
    Side = 1

    def toSentioAbbr(self):
        switcher = {LoadPosition.Front: "front", LoadPosition.Side: "side"}
        return switcher.get(self, "Invalid Load position")


class Module(Enum):
    """An enumerator containing the names of all SENTIO modules.

    Module availability is determined by the specific type of probe station.
    All probe stations have the dashboard, setup and service modules. Most likely
    wafermap and Vision module will also be present (unless you have a purely manual
    station)

    Attributes:
        Wafermap (0): The wafermap module. This module is used for wafer alignment and wafer mapping.
        Vision (1): The vision module. This module is used for die alignment and wafer inspection.
        Setup (2): The setup module. This module is used for setting up the probe station.
        Service (3): The service module. This module is used for service and maintenance.
        Qalibria (4): The Qalibria module. This module is used for Qalibria integration.
        AuxSites (5): The aux site module. This module is used for auxilliary site integration.
        Loader (6): The loader module. This module is used for loader integration.
        Dashboard (7): The dashboard module. This module is used for dashboard integration.
    """

    Wafermap = 0
    Vision = 1
    Setup = 2
    Service = 3
    Qalibria = 4
    AuxSites = 5
    Loader = 6
    Dashboard = 7

    def toSentioAbbr(self):
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


@deprecated(reason="duplicated; Use CompensationMode instead.")
class OnTheFlyMode(Enum):
    Lateral = 0
    Vertical = 1
    Both = 2
    ProbeCard = 3

    def toSentioAbbr(self):
        switcher = {
            OnTheFlyMode.Lateral: "AlignDie",
            OnTheFlyMode.Vertical: "MapScan",
            OnTheFlyMode.Both: "Topography",
            OnTheFlyMode.ProbeCard: "ProbeCard",
        }
        return switcher.get(self, "Invalid OTF mode")


class OrientationMarker(Enum):
    """Defines the wafers orientation marker.

    Orientation markers can either be a notch or a flat in the wafer.
    The orientation marker is used by the prealigner to detect
    the wafer position.

    Today mostly notches are used ar orientation markes as they reduce the
    waste of wafer space.

    Attributes:
        Notch (0): Wafer uses a notch.
        Flat (1): Wafer uses a flat.
    """

    Notch = 0
    Flat = 1

    def toSentioAbbr(self):
        switcher = {OrientationMarker.Notch: "Notch", OrientationMarker.Flat: "Flat"}
        return switcher.get(self, "Invalid orientation marker")


class PoiReferenceXy(Enum):
    """Referenc position for points of interest.

    Each point of interest can either be defines with respect to the center of the stage.
    Or with respect to the center of the die.

    Attributes:
        DieCenter (0): Use die center as the position reference.
        StageCenter (1): Use stage center as the position reference.
    """

    DieCenter = 0
    StageCenter = 1

    def toSentioAbbr(self):
        switcher = {
            PoiReferenceXy.DieCenter: "DieCenter",
            PoiReferenceXy.StageCenter: "StageCenter",
        }
        return switcher.get(self, "Invalid stage")


class ProjectFileInfo(Enum):
    """An enumerator containing the different aspects of retrieving current project info.

    Attributes:
        NameOnly (0): Return only the project name.
        FullPath (1): Return the full path to the project file.
    """

    NameOnly = 0
    FullPath = 1

    def toSentioAbbr(self):
        switcher = {
            ProjectFileInfo.NameOnly: "Name",
            ProjectFileInfo.FullPath: "FullPath",
        }
        return switcher.get(self, "Invalid ProjectFileInfo")


class PtpaType(Enum):
    """Defines the type of Probe to Pad Alignment used by SENTIO.

    Attributes:
        OffAxis (0): Use off-axis PTPA with the platen camera and the chuck camera looking up to the probe tips.
        OnAxis (1): Use on axis PTPA with the scope camera looking down on the probe tips.
    """

    OffAxis = 0
    OnAxis = 1

    def toSentioAbbr(self):
        switcher = {PtpaType.OffAxis: "offaxis", PtpaType.OnAxis: "onaxis"}
        return switcher.get(self, "Invalid ptpa type")


class SnapshotType(Enum):
    """Specifies the type of image snapshot to be taken"""

    CameraRaw = 0
    """ The snapshot is the raw image from the camera in original resolution """

    WithOverlays = 1
    """ The snapshot consists of a screenshot of the vision module inside SENTIO. This method 
        will also contain the overlays displayed by the vision module but the image resolution
        will be whatever the current resolution of SENTIO's vision module is. """

    def toSentioAbbr(self):
        """Turn the SnapshotType into a string that can be used as a parameter for SENTIO's snap_image command."""
        switcher = {SnapshotType.CameraRaw: "0", SnapshotType.WithOverlays: "1"}
        return switcher.get(self, "Invalid SnapshotType type")


class SnapshotLocation(Enum):
    """Specifies where a snapshot shall be saved."""

    Prober = 0
    """ The snapshot is stored remotely on the prober PC that is executing SENTIO. """

    Local = 1
    """ The snapshot will be transferred to the PC that is running the python control script. 
        This option only makes sense if the prober and the control PC are different. """


class Stage(Enum):
    """Represents a stage in SENTIO.

    A stage is a piece of hardware that can be controlled by motors and moved in x, y and
    probably also z direction.

    Attributes:
        Chuck (0): The chuck stage. This is where the wafer is placed.
        Scope (1): The scope stage controls the downward looking microscope. This is an optional stage but it will be present on most probe stations.
        Vce (2): First Vce stage. Vce Stages can only be moved in z-direction.
        Vce2 (3): Second Vce stage. Vce Stages can only be moved in z-direction.
        Probe1 (4): First motorized probe.
        Probe2 (5): Second motorized probe.
        Probe3 (6): Third motorized probe.
        Probe4 (7): Fourth motorized probe.
    """

    Chuck = 0
    Scope = 1
    Vce = 2
    Vce2 = 3
    Probe1 = 4
    Probe2 = 5
    Probe3 = 6
    Probe4 = 7

    def toSentioAbbr(self):
        switcher = {
            Stage.Chuck: "chuck",
            Stage.Scope: "scope",
            Stage.Vce: "vce01",
            Stage.Vce2: "vce02",
            Stage.Probe1: "Probe01",
            Stage.Probe2: "Probe02",
            Stage.Probe3: "Probe03",
            Stage.Probe4: "Probe04",
        }
        return switcher.get(self, "Invalid stage")


class SteppingContactMode(Enum):
    """This mode defines how the chuck behaves during steeping.

    Attributes:
        BackToContact (0): Chuck will move back to contact position after stepping.
        StepToSeparation (1): Chuck will move to separation position after stepping.
        LockContact (2): Chuck cannot step when at contact. You will have to manually move it away from its contact position before issuing the next step command.
    """

    BackToContact = 0
    StepToSeparation = 1
    LockContact = 2

    def toSentioAbbr(self):
        switcher = {
            SteppingContactMode.BackToContact: "BackToContact",
            SteppingContactMode.StepToSeparation: "StepToSeparation",
            SteppingContactMode.LockContact: "LockContact",
        }
        return switcher.get(self, "Invalid stepping mode")


class TestSelection(Enum):
    """Specifies which dies shall be selected for test.

    If a die is selected for test it is activated in the wafer map.

    Attributes:
        Nothing (0): Select no dies.
        Good (1): Select only the good dies.
        GoodAndUgly (2): Select only the good dies. Ugly dies are the dies with at least one corner in the edge area of the map. The are completely present on the wafer but may be damaged or have incomplete structures.
        GoodUglyAndEdge (3): Good dies are the dies that are completely within the wafer map with no edge lying in the edge area of the map. Ugly dies are the dies with at least one corner in the edge area of the map. The are completely present on the wafer but may be damaged or have incomplete structures. The dies with at leas one edge outside of the wafer are called edge dies. Those dies are incomplete.
        All (4): Select all dies for testing.
    """

    Nothing = 0
    Good = 1
    GoodAndUgly = 2
    GoodUglyAndEdge = 3
    All = 4

    def toSentioAbbr(self):
        switcher = {
            TestSelection.Nothing: "n",
            TestSelection.Good: "g",
            TestSelection.GoodAndUgly: "u",
            TestSelection.GoodUglyAndEdge: "e",
            TestSelection.All: "a",
        }
        return switcher.get(self, "Invalid TestSelection")


class ScopeXYReference(Enum):
    """Position reference for scope motions.

    Attributes:
        Zero (0): Use absolute scope coordinates.
        Home (1): Use coordinates with respect to the scope home position.
        Relative (2): Use coordinates with respect to the current scope position.
    """

    Zero = 0
    Home = 1
    Relative = 2

    def toSentioAbbr(self):
        switcher = {
            ScopeXYReference.Zero: "Z",
            ScopeXYReference.Home: "H",
            ScopeXYReference.Relative: "R",
        }
        return switcher.get(self, "Invalid scope xy reference")


class ScopeZReference(Enum):
    """Scope z reference for scoep motions.

    Attributes:
        Zero (0): Use absolute scope coordinates.
        Relative (1): Use coordinates with respect to the current scope position.
    """

    Zero = 0
    Relative = 1

    def toSentioAbbr(self):
        switcher = {ScopeZReference.Zero: "Z", ScopeZReference.Relative: "R"}
        return switcher.get(self, "Invalid scope z reference")


class ProbeSentio(Enum):
    """An enumeration containing a list of position for motorized probes.

    Attributes:
        East (0): Probe is on the right side of the chuck.
        West (1): Probe is on the left side of the chuck.
        North (2): Probe is at the back side of the prober.
        South (3): Probe is on the front side of the prober.
    """

    East = 0
    West = 1
    North = 2
    South = 3

    def toSentioAbbr(self):
        switcher = {
            ProbeSentio.East: "East",
            ProbeSentio.West: "West",
            ProbeSentio.North: "North",
            ProbeSentio.South: "South",
        }
        return switcher.get(self, "Invalid ProbeSentio enumerator")


class ProbeXYReference(Enum):
    """Position reference for mororized probe movements.

    Attributes:
        Zero (0): Use absolute probe coordinates.
        Home (1): Use coordinates with respect to the probe home position.
        Current (2): Use coordinates with respect to the current probe position.
    """

    Zero = 0
    Home = 1
    Current = 2

    def toSentioAbbr(self):
        switcher = {
            ProbeXYReference.Zero: "Zero",
            ProbeXYReference.Home: "Home",
            ProbeXYReference.Current: "Current",
        }
        return switcher.get(self, "Invalid probe xy reference")


class ProbeZReference(Enum):
    """Position reference for probe z motions.

    Attributes:
        Zero (0): Use absolute probe coordinates.
        Current (1): Use coordinates with respect to the current probe position.
        Contact (2): Use coordinates with respect to the contact height.
        Separation (3): Use coordinates with respect to the separation height.
    """

    Zero = 0
    Current = 1
    Contact = 2
    Separation = 3

    def toSentioAbbr(self):
        switcher = {
            ProbeZReference.Zero: "Zero",
            ProbeZReference.Current: "Current",
            ProbeZReference.Contact: "Contact",
            ProbeZReference.Separation: "Separation",
        }
        return switcher.get(self, "Invalid probe z reference")


class PtpaFindTipsMode(Enum):
    """Specifies the mode used by ptpa tip finding.

    Attributes:
        OnAxis (0): Use on axis tip finding.
        OffAxis (1): Use off axis tip finding.
    """

    OnAxis = 0
    OffAxis = 1

    def toSentioAbbr(self):
        switcher = {
            PtpaFindTipsMode.OnAxis: "OnAxis",
            PtpaFindTipsMode.OffAxis: "OffAxis",
        }
        return switcher.get(self, "Invalid PTPA_Find_Tips_Mode function")


class RemoteCommandError:
    """A list of possible error codes used by SENTIO.

    This list may not contain the full list of codes used by SENTIO due to
    the fact that SENTIO is a moving target and new error codes may be added
    or removed.

    Have a look at the remote command specification to see which codes are
    supported by your version.

    Attributes:
        NoError (0): No error occured.
        InternalError (1): An internal error occured in SENTIO. This is not supposed to happen and you can probably not fix the issue on your own. Please contact SENTIO support.
        ExecutionError (2): A generic execution error. This is the most widely used error code to signal remote command failure.
        CommandHandlerNotFound (3): A command handler for a certain subsystem of SENTIO was not found. This may happen when sending commands to a SENTIO module that is not available on a given machine.
        InvalidCommand (4): not used by SENTIO's native remote command set.
        InvalidCommandFormat (5): not used by SENTIO's native remote command set.
        InvalidParameter (6): A remote command parameter is incoreect.
        InvalidNumberOfParameters (7): The number of submitted remote command parameters is incorect.
        ArgumentOutOfBounds (8): A submitted parameter exceeds the range of allowed values.
        FileNotFound (9): A file that was supposed to be loaded by SENTIO was not found.
        InvalidFileFormat (10): not used by SENTIO's native remote command set.
        EndOfRoute (11): Stepping reached the end of the route.
        InvalidOperation (12): The requested operation is not allowed in the current state.
        NotSupported (13): The requested operation is not supported by the current version of SENTIO.
        SubsiteNotRoutable (14): The requested subsite is not routable.
        ProjectRequired (15): A requested operation require an active project.
        Unused (16): This error code is unused.
        PrealignmentFailed (17): Prealignment failed.
        HomePositionNotSet (18): The home position is not set.
        Timeout (19): A command or operation timed out.
        PatternNotTrained (20): A required pattern is not trained
        PatternNotFound (21): A pattern could not be found
        TooManyPatternsFound (22): Too many patterns were found
        ContactHeightNotSet (23): The contact height is not set.
        AutoFocusFailed (24): Auto focus failed on the wafer.
        TipFocusFailed (25): Auto focus failed on the tips.
        TipNotFound (26): A tip could not be found.
        OffsetOverTolerance (27): The offset is over tolerance.
        CommandPending (30): Returned when the status of an async command is polled with query_command_status and the command is Running
        AsyncCommandAborted (31): Returned when a async command was aborted prematurely
        UnknownCommandId (32): Returned when an async command is queried but SENTIO does not know anything about this command id
        CameraNotCalibrated (35): A camera required for a vision task is not calibrated
        CameraDoesNotExist (36): A required camera is not installed in the system.
        AlignAccuracyBad (37): Alignment accuracy over 10 µm
        SteppingWithWrongZPosition (38): Stepping when Chuck is below Separation
        FrontDoorOpen (60): The front load door is open
        LoaderDoorOpen (61): The side door is open
        FrontDoorLockFail (62): Front door lock cannot be engaged
        LoaderDoorLockFail (63): Side door lock cannot be engaged
        SlotOrStationOccupied (64): A slot or station that is the target of a wafer transfer is already occupied
        SlotOrStationEmpty (65): A slot or station that is the origin of a wafer transfer does not have a wafer
        ProbeBackDoorOpen (66): The probe back door is open
        ProbeSideDoorOpen (67): The probe side door is open (Not loader door, only TS2500/SE has this door, the door near the probe back door)
        VacuumFailed (68): Vacuum failed
        LoaderTrayDoorOpen (69): The tray door is open
        LoaderCassetteDoesNotExist (80): The cassette does not exist
        LoaderSlotNumberError (81): The slot number is not correct
        LoaderPreAlignerAngleError (83): The prealigner angle is not correct
    """

    NoError = 0
    InternalError = 1
    ExecutionError = 2
    CommandHandlerNotFound = 3
    InvalidCommand = 4
    InvalidCommandFormat = 5
    InvalidParameter = 6
    InvalidNumberOfParameters = 7
    ArgumentOutOfBounds = 8
    FileNotFound = 9
    InvalidFileFormat = 10
    EndOfRoute = 11
    InvalidOperation = 12
    NotSupported = 13
    SubsiteNotRoutable = 14
    ProjectRequired = 15
    EndOfList = 16
    PrealignmentFailed = 17
    HomePositionNotSet = 18
    Timeout = 19
    PatternNotTrained = 20
    PatternNotFound = 21
    TooManyPatternsFound = 22
    ContactHeightNotSet = 23
    AutoFocusFailed = 24
    TipFocusFailed = 25
    TipNotFound = 26
    OffsetOverTolerance = 27
    CommandPending = 30
    AsyncCommandAborted = 31
    UnknownCommandId = 32
    CameraNotCalibrated = 35
    CameraDoesNotExist = 36
    AlignAccuracyBad = 37
    SteppingWithWrongZPosition = 38
    FrontDoorOpen = 60
    LoaderDoorOpen = 61
    FrontDoorLockFail = 62
    LoaderDoorLockFail = 63
    SlotOrStationOccupied = 64
    SlotOrStationEmpty = 65
    ProbeBackDoorOpen = 66
    ProbeSideDoorOpen = 67
    VacuumFailed = 68
    LoaderTrayDoorOpen = 69
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


class RoutingPriority(Enum):
    """Defines the stepping order.

    Attributes:
        RowUniDir (0): Rows first always step in same direction.
        ColUniDir (1): Columns first always step in same direction.
        RowBiDir (2): Rows first. Step odd rows backwards.
        ColBiDir (3): Columns first. Step odd columns backwards.
    """

    RowUniDir = 0
    ColUniDir = 1
    RowBiDir = 2
    ColBiDir = 3

    def toSentioAbbr(self):
        switcher = {
            RoutingPriority.RowUniDir: "r",
            RoutingPriority.ColUniDir: "c",
            RoutingPriority.RowBiDir: "wr",
            RoutingPriority.ColBiDir: "wc",
        }
        return switcher.get(self, "Invalid RoutingPriority enumerator")


class RoutingStartPoint(Enum):
    """Defines the starting point for routing (stepping commands).

    Attributes:
        UpperLeft (0): Stepping starts in upper left corner of the map.
        UpperRight (1): Stepping starts in upper right corner of the map.
        LowerLeft (2): Stepping stars in lower left corner of the map.
        LowerRight (3): Stepping starts in lower right corner of the map.
    """

    UpperLeft = 0
    UpperRight = 1
    LowerLeft =  2
    LowerRight = 3

    def toSentioAbbr(self):
        switcher = {
            RoutingStartPoint.UpperLeft: "ul",
            RoutingStartPoint.UpperRight: "ur",
            RoutingStartPoint.LowerLeft: "ll",
            RoutingStartPoint.LowerRight: "lr",
        }
        return switcher.get(self, "Invalid RoutingStartPoint enumerator")


class StatusBits:
    """List of status codes used by SENTIO.

    SENTIO will encode certain status information into the error code variable.
    This status information does not represent an errors but rather a machine
    status.

    Attributes:
        EndOfRoute (1): Stepping reached the end of the route.
        LastSite (2): Stepping reached the last site of a die.
    """

    EndOfRoute = 1
    LastSite = 2


class SoftwareFence(Enum):
    """An enumerator holding software fence implementations.

    Attributes:
        Disabled (0): Fence is disabled.
        Round (1): A round fence around the chuck, excluding aux sites.
        Rectangle (2): A rectangular fence around the chuck, may include parts of the aux sites.
        SoftwareLimit (3): Use software limits on axis. A Large rectangular fence around the chuck motion ares. Collisions with the prober housing are possible (TS-2000; tilted front door)
    """

    Disabled = 0
    Round = 1
    Rectangle = 2
    SoftwareLimit = 3

    def toSentioArg(self):
        switcher = {
            SoftwareFence.Disabled: "Disable",
            SoftwareFence.Rectangle: "Rectangle",
            SoftwareFence.Round: "Round",
            SoftwareFence.SoftwareLimit: "SoftwareLimit",
        }
        return switcher.get(self, "Invalid SoftwareFence parameter")


class ThermoChuckState(Enum):
    """The state of a thermo chuck.

    Attributes:
        Soaking (0): The chuck is in soaking state,
        Cooling (1): The chuck is in cooling state,
        Heating (2): The chuck is in heating state,
        Uncontrolled (3): The chuck is in uncontrolled state,
        Standby (4): The chuck is in standby state,
        Error (5): The chuck is in error state,
        Controlling (6): The chuck is in controlling state,
    """

    Soaking = 0
    Cooling = 1
    Heating = 2
    Uncontrolled = 3
    Standby = 4
    Error = 5
    Controlling = 6
    Unknown = 7


class VceZReference(Enum):
    """Reference for Vce z motions.

    Attributes:
        Zero (0): Use absolute Vce coordinates.
        Relative (1): Use coordinates with respect to the current Vce position.
    """

    Zero = 0
    Relative = 1

    def toSentioAbbr(self):
        switcher = {VceZReference.Zero: "Z", VceZReference.Relative: "R"}
        return switcher.get(self, "Invalid vce z reference")


class VirtualCarrierInitFlags(Enum):
    """Flags for initializing a virtual carrier measurement.

    Attributes:
        Start (0): Start a new virtual carrier measurement.
        Continue (1): Continue an existing virtual carrier measurement. If no measurement is running, this will start a new one.
    """

    Start = 0
    Continue = 1

    def toSentioAbbr(self):
        switcher = {
            VirtualCarrierInitFlags.Start: "Start",
            VirtualCarrierInitFlags.Continue: "Continue",
        }
        return switcher.get(self, "Invalid VirtualCarrierInitFlags")


class VirtualCarrierStepProcessingState(Enum):
    """State of a single virtual carrier processing step. 
    
    Attributes:
        Skip (0): The step is skipped.
        Done (1): The step is done.
        Ready (2): The step is ready to be executed.
    """
    Skip = 0
    Done = 1
    Ready = 2

    def toSentioAbbr(self):
        switcher = {
            VirtualCarrierStepProcessingState.Skip: "Skip",
            VirtualCarrierStepProcessingState.Done: "Done",
            VirtualCarrierStepProcessingState.Ready: "Ready",
        }
        return switcher.get(self, "Invalid VirtualCarrierStepProcessingState")


class WorkArea(Enum):
    """An enumeration containing probe station work areas. The OffAxis work area is only present if the specific model of probe station supports it.

    Attributes:
        Probing (0): The probing work area is the area in which the chuck is under the downward looking microscope. This is where the wafer is probed.
        Offaxis (1): The off axis work area is the area in which the chuck is under the off axis camera. This is where off axis ptpa is performed. The wafer cannot be probed here because there is no probe card.
    """

    Probing = 0
    Offaxis = 1

    def toSentioAbbr(self):
        switcher = {
            WorkArea.Probing: "Probing",
            WorkArea.Offaxis: "Offaxis",
        }
        return switcher.get(self, "Invalid chuck site")


class ZPositionHint(Enum):
    """Represents a hint for the z position of a stage.

    Not all values are used by all stages. A scope does not have a contact height
    and a chuck Hover height may be disabled by SENTIO.

    Attributes:
        Default (0): Used internally only. Essentially means the value is unset or undefined.
        Contact (1): Stage is at contact position.
        Hover (2): Stage is at hover position.
        Separation (3): Stage is at separation position
        Lift (4): Stage is at Lift position.
        Transfer (5): Chuck is at transfer position. This is used for the chuck only when the loader is doing a wafer transfer internally.
    """

    Default = 0
    Contact = 1
    Hover = 2
    Separation = 3
    Lift = 4
    Transfer = 5

    def toSentioAbbr(self):
        switcher = {
            ZPositionHint.Default: "Default",
            ZPositionHint.Contact: "Contact",
            ZPositionHint.Hover: "Hover",
            ZPositionHint.Separation: "Separation",
            ZPositionHint.Lift: "Lift",
            ZPositionHint.Transfer: "Transfer",
        }
        return switcher.get(self, "Invalid ZPositionHint")
