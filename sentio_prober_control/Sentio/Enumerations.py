from enum import Enum

class CompensationMode(Enum):
    Lateral = 0,
    Vertical = 1,
    Both = 2,
    ProbeCard = 3

    def toSentioAbbr(self):
        switcher = {
            CompensationMode.Lateral: "Lateral",
            CompensationMode.Vertical: "Vertical",
            CompensationMode.Both: "Both",
            CompensationMode.ProbeCard: "ProbeCard"
        }
        return switcher.get(self, "Invalid CompensationMode")

class CompensationType(Enum):
    DieAlign = 0,
    Topography = 1,
    MapScan = 2,
    AlignDie = 3,
    SkateDetection = 4

    def toSentioAbbr(self):
        switcher = {
            CompensationType.DieAlign: "DieAlign",
            CompensationType.Topography: "Topography",
            CompensationType.MapScan: "MapScan",
            CompensationType.AlignDie: "AlignDie",
            CompensationType.SkateDetection: "SkateDetection"
        }
        return switcher.get(self, "Invalid CompensationType")

class ProjectFileInfo(Enum):
    NameOnly = 0,
    FullPath = 1,

    def toSentioAbbr(self):
        switcher = {
            ProjectFileInfo.NameOnly: "Name",
            ProjectFileInfo.FullPath: "FullPath"
        }
        return switcher.get(self, "Invalid ProjectFileInfo")


class DefaultPattern(Enum):
    Align = 0,
    Home = 1,
    DieAlignPos1 = 3,
    DieAlignPos2 = 4,
    TwoPoint = 5,
    Vce = 6,
    Ptpa = 7,

    def toSentioAbbr(self):
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


class SteppingContactMode(Enum):
    BackToContact = 0,
    StepToSeparation = 1,
    LockContact = 2,

    def toSentioAbbr(self):
        switcher = {
            SteppingContactMode.BackToContact: "BackToContact",
            SteppingContactMode.StepToSeparation: "StepToSeparation",
            SteppingContactMode.LockContact:   "LockContact"
        }
        return switcher.get(self, "Invalid stepping mode")


class Stage(Enum):
    Chuck = 0,
    Scope = 1,
    Vce = 2,
    Vce2 = 3,
    Probe1 = 4,
    Probe2 = 5,
    Probe3 = 6,
    Probe4 = 7

    def toSentioAbbr(self):
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
    DieCenter = 0,
    StageCenter = 1

    def toSentioAbbr(self):
        switcher = {
            PoiReferenceXy.DieCenter: "DieCenter",
            PoiReferenceXy.StageCenter: "StageCenter"
        }
        return switcher.get(self, "Invalid stage")


class PtpaType(Enum):
    OffAxis = 0,
    OnAxis = 1,

    def toSentioAbbr(self):
        switcher = {
            PtpaType.OffAxis: "offaxis",
            PtpaType.OnAxis: "onaxis"
        }
        return switcher.get(self, "Invalid ptpa type")


class TestSelection(Enum):
    Nothing = 0,
    Good = 1,
    GoodAndUgly = 2,
    GoodUglyAndEdge = 3,
    All = 4


class DetectionCoordindates(Enum):
    Image = 0,
    Fov = 1,
    Roi = 2

    def toSentioAbbr(self):
        switcher = {
            DetectionCoordindates.Image: "Image",
            DetectionCoordindates.Fov: "Fov",
            DetectionCoordindates.Roi: "Roi"
        }
        return switcher.get(self, "Invalid ProbeTipDetector")


class DetectionAlgorithm(Enum):
    Keypoint = 0,            
    ProbeTip = 1,            # deprecated; subject to future removal   
    ProbeTipFromBelow = 2,   # deprecated; subject to future removal   
    VerticalProbeCard = 3,   # deprecated; subject to future removal   
    PyramidTipRingLight = 4, # deprecated; subject to future removal   
    PyramidTipSpotLight = 5, # deprecated; subject to future removal   
    ProbeDetector = 6,
    WaferDetector = 7

    def toSentioAbbr(self):
        switcher = {
            DetectionAlgorithm.Keypoint: "Keypoint",
            DetectionAlgorithm.ProbeTip: "ProbeTip",
            DetectionAlgorithm.ProbeTipFromBelow: "ProbeTipFromBelow",
            DetectionAlgorithm.VerticalProbeCard: "VerticalProbeCard",
            DetectionAlgorithm.PyramidTipRingLight: "PyramidTipRingLight",
            DetectionAlgorithm.PyramidTipSpotLight: "PyramidTipSpotLight",
            DetectionAlgorithm.ProbeDetector: "ProbeDetector",
            DetectionAlgorithm.WaferDetector: "WaferDetector"
        }
        return switcher.get(self, "Invalid ProbeTipDetector")


class Module(Enum):
    Wafermap = 0,
    Vision = 1,
    Setup = 2,
    Service = 3,
    Qalibria = 4,
    AuxSites = 5,
    Loader = 6,
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


class AxisOrient(Enum):
    DownRight = 0,
    DownLeft = 1,
    UpRight = 2,
    UpLeft = 3

    def toSentioAbbr(self):
        switcher = {
            AxisOrient.DownRight: "DR",
            AxisOrient.DownLeft: "DL",
            AxisOrient.UpRight: "UR",
            AxisOrient.UpLeft: "UL"
        }
        return switcher.get(self, "Invalid AxisOrient")


class DieNumber(Enum):
    Present = 1,
    Selected = 2


class ColorScheme(Enum):
    ColorFromBin = 0,
    ColorFromValue = 1

    def toSentioAbbr(self):
        switcher = {
            ColorScheme.ColorFromBin: 0,
            ColorScheme.ColorFromValue: 1
        }
        return switcher.get(self, "Invalid ColorScheme")

class OrientationMarker(Enum):
    Notch = 0,
    Flat = 1

    def toSentioAbbr(self):
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
        switcher = {
            AutoAlignCmd.AutoDieSize: "auto",
            AutoAlignCmd.UpdateDieSize: "update",
            AutoAlignCmd.TwoPt: "2pt",
            AutoAlignCmd.CurrentDieSize: ""
        }
        return switcher.get(self, "Invalid Auto Align function")

class ScopeXYReference(Enum):
    Zero = 0,
    Home = 1,
    Relative = 2

    def toSentioAbbr(self):
        switcher = {
            ScopeXYReference.Zero: "Z",
            ScopeXYReference.Home: "H",
            ScopeXYReference.Relative: "R"
        }
        return switcher.get(self, "Invalid scope xy reference")


class ScopeZReference(Enum):
    Zero = 0,
    Relative = 1

    def toSentioAbbr(self):
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
        switcher = {
            AutoFocusAlgorithm.Gradient: "Gradient",
            AutoFocusAlgorithm.Bandpass: "Bandpass",
            AutoFocusAlgorithm.Difference: "Difference",
            AutoFocusAlgorithm.AutoCorrelation: "AutoCorrelation"
        }
        return switcher.get(self, "Invalid focus measure")


class ChuckXYReference(Enum):
    Zero = 0,
    Home = 1,
    Relative = 2,
    Center = 3,
    User = 4,

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
    Zero = 0,
    Relative = 1,
    Contact = 2,
    Hover = 3,
    Separation = 4

    def toSentioAbbr(self):
        switcher = {
            ChuckZReference.Zero: "Z",
            ChuckZReference.Relative: "R",
            ChuckZReference.Contact: "C",
            ChuckZReference.Hover: "H",
            ChuckZReference.Separation: "S"
        }
        return switcher.get(self, "Invalid chuck z reference")


class ChuckThetaReference(Enum):
    Zero = 0,
    Site = 1,
    Relative = 2

    def toSentioAbbr(self):
        switcher = {
            ChuckThetaReference.Zero: "Z",
            ChuckThetaReference.Site: "S",
            ChuckThetaReference.Relative: "R"
        }
        return switcher.get(self, "Invalid chuck theta reference")


class WorkArea(Enum):
    Probing = 0,
    Offaxis = 1,

    def toSentioAbbr(self):
        switcher = {
            WorkArea.Probing: "Probing",
            WorkArea.Offaxis: "Offaxis",
        }
        return switcher.get(self, "Invalid chuck site")


class ChuckSite(Enum):
    Wafer = 0,
    AuxRight = 1,
    AuxLeft = 2,
    AuxRight2 = 3,
    AuxLeft2 = 4,
    ChuckCamera = 5,

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


class LoaderStation(Enum):
    Cassette1 = 0,
    Cassette2 = 1,
    PreAligner = 2,
    Chuck = 3,
    ForkA = 4,
    ForkB = 5,
    WaferWallet = 6,
    IdReader = 7

    def toSentioAbbr(self):
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
        switcher = {
            ProbeZReference.Zero: "Z",
            ProbeZReference.Relative: "R",
        }
        return switcher.get(self, "Invalid chuck z reference")


class CameraMountPoint(Enum):
    Scope = 0,
    Chuck = 1,
    OffAxis = 2,
    Vce = 3,
    Scope2 = 4,

    def toSentioAbbr(self):
        switcher = {
            CameraMountPoint.Scope: "scope",
            CameraMountPoint.Chuck: "chuck",
            CameraMountPoint.OffAxis: "offaxis",
            CameraMountPoint.Vce: "vce01",
            CameraMountPoint.Scope2: "scope2"
        }
        return switcher.get(self, "Invalid camera mount point id")


class ChuckPositionHint(Enum):
    Center = 0,
    FrontLoad = 1,
    SideLoad = 2

#    def toSentioAbbr(self):
#        switcher = {
#            ChuckPositionHint.Center: "Wafer",
#            ChuckPositionHint.FrontLoad: "AuxLeft",
#            ChuckPositionHint.SideLoad: "AuxLeft2",
#        }
#        return switcher.get(self, "Invalid chuck position hint")

class BinSelection(Enum):
    All = 0,
    DiesOnly = 1,
    SubsitesOnly = 2


class RoutingPriority(Enum):
    RowUniDir = 0,
    ColUniDir = 1,
    RowBiDir = 2,
    ColBiDir = 3


class RoutingStartPoint(Enum):
    UpperLeft = 0,
    UpperRight = 1,
    LowerLeft = 2,
    LowerRight = 3


class StatusBits:
    EndOfRoute = 1
    LastSite = 2


# Remote command errors for Sentio 3.0
class RemoteCommandError:
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
        TransferSlotOccupied = 15
        TransferSlotEmpty = 16
        PrealignmentFailed = 17
        IsBusy = 18
        Timeout = 19
        PatternNotTrained = 20
        PatternNotFound = 21
        UnknownCommandId = 22
        AsyncCommandAborted = 24
        CameraNotCalibrated = 25
        CommandPending = 30
        FrontDoorOpen = 60
        LoaderDoorOpen = 61
        FrontDoorLockFail = 62
        LoaderDoorLockFail = 63
        WaferExisting = 64
        WaferNotExisting = 65


class FindPatternReference(Enum):
    DieHome = 0,
    CenterOfRoi = 1

    def toSentioAbbr(self):
        switcher = {
            FindPatternReference.DieHome: "DieHome",
            FindPatternReference.CenterOfRoi: "CenterOfRoi"
        }
        return switcher.get(self, "Invalid find pattern reference id")


class DialogButtons(Enum):
    Ok = 1,
    Cancel = 2,
    OkCancel = 3

    def toSentioAbbr(self):
        switcher = {
            DialogButtons.Ok: "Ok",
            DialogButtons.Cancel: "Cancel",
            DialogButtons.OkCancel: "OkCancel"
        }
        return switcher.get(self, "Invalid button id")


class LoadPosition(Enum):
    Front = 0,
    Side = 1

    def toSentioAbbr(self):
        switcher = {
            LoadPosition.Front: "front",
            LoadPosition.Side: "side"
        }
        return switcher.get(self, "Invalid Load position")


class VceZReference(Enum):
    Zero = 0,
    Relative = 1

    def toSentioAbbr(self):
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
        switcher = {
            ProbeSentio.East: "East",
            ProbeSentio.West: "West",
            ProbeSentio.North: "North",
            ProbeSentio.South: "South"
        }
        return switcher.get(self, "Invalid Probe reference")


class Compensation(Enum):
    Lateral = 0,
    Vertical = 1,
    Both = 2,
    ProbeCard = 3,
    MapScan = 4,
    Thermal = 5,
    Topography =6,

    def toSentioAbbr(self):
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


class ExecuteCompensation(Enum):
    AlignDie = 0,
    MapScan = 1,
    Topography =2,

    def toSentioAbbr(self):
        switcher = {
            ExecuteCompensation.AlignDie: "AlignDie",
            ExecuteCompensation.MapScan: "MapScan",
            ExecuteCompensation.Topography: "Topography",
        }
        return switcher.get(self, "Invalid compensation type")


class OnTheFlyMode(Enum):
    Lateral = 0,
    Vertical = 1,
    Both =2,
    ProbeCard =3,

    def toSentioAbbr(self):
        switcher = {
            OnTheFlyMode.Lateral: "AlignDie",
            OnTheFlyMode.Vertical: "MapScan",
            OnTheFlyMode.Both: "Topography",
            OnTheFlyMode.ProbeCard: "ProbeCard",
        }
        return switcher.get(self, "Invalid OTF mode")

class ExecuteAction(Enum):
    Execute = 0,
    Abort = 1,

    def toSentioAbbr(self):
        switcher = {
            ExecuteAction.Execute: "execute",
            ExecuteAction.Abort: "abort",
        }
        return switcher.get(self, "Invalid ExecuteAction function")

class PtpaFindTipsMode(Enum):
    OnAxis = 0,
    OffAxis = 1,

    def toSentioAbbr(self):
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
        switcher = {
            DieCompensationMode.Lateral: "Lateral",
            DieCompensationMode.Vertical: "Vertical",
            DieCompensationMode.Both: "Both",
            DieCompensationMode.ProbeCard: "ProbeCard",
            DieCompensationMode.SkateDetection: "SkateDetection",
        }
        return switcher.get(self, "Invalid DieCompensationMode function")
    
class ZPositionHint(Enum):
    Default = 0,
    Contact = 1,
    Hover = 2,
    Separation = 3,
    Lift = 4,
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
