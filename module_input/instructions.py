from module_input.LoadTaskMovieFile import LoadTaskMovieFile
from module_input.LoadTaskPictureFile import LoadTaskPictureFile
from module_input.LoadTaskCurves import LoadTaskCurves
from module_input.Curve.CurveExtraction import CurveExtraction
from module_input.Curve.Csv.LoadOptionsCsv import LoadOptionsCsv
from module_input.Curve.Binout.LoadCurvesSelectionBinout import LoadCurvesSelectionBinout
from module_input.Curve.Crv.LoadCurvesSelectionCrv import LoadCurvesSelectionCrv
from module_input.Curve.Csv.LoadCurvesSelectionCsv import LoadCurvesSelectionCsv


instructions = [
    LoadTaskCurves({}),
    LoadTaskPictureFile({}),
    LoadTaskMovieFile({}),
    CurveExtraction({}),
    LoadCurvesSelectionBinout({}),
    LoadCurvesSelectionCrv({}),
    LoadCurvesSelectionCsv({}),
    LoadOptionsCsv({})
]
