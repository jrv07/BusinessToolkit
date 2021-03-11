from module_input.LoadTaskFile import LoadTaskFile
from module_input.Curve.CurveExtraction import CurveExtraction
from module_misc.RegisterData import RegisterCalculationData
from module_misc.Curves import Curves
from module_input.Curve.Binout.CurveLoaderBinout import CurveLoaderBinout
from module_input.Curve.Crv.CurveLoaderCrv import CurveLoaderCrv
from module_input.Curve.Csv.CurveLoaderCsv import CurveLoaderCsv
from module_input.Curve.CurveLoader import CurveLoader
import logging


class LoadTaskCurves(LoadTaskFile):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._curve_loader: CurveLoader = None
        self._log_curve_tags = None
        self._curve_extraction_input = None
        self._curve_extraction: CurveExtraction = None
        self._curves = Curves()
        self._extractor.add_bool("log_curve_tags", description="")
        self._extractor.add_object("curve_extraction", CurveExtraction, optional=False, description="")

    def generate_curve_extraction(self):
        curve_extraction = CurveExtraction(self._curve_extraction_input)
        curve_extraction.generate()
        self._curve_extraction = curve_extraction

    def generate_curve_loader(self):
        curve_type = self._curve_extraction.type
        selections = self._curve_extraction.selections
        options = self._curve_extraction.options
        if curve_type == "binout":
            curve_loader = CurveLoaderBinout(self._file_path, selections, self._log_curve_tags)
        elif curve_type == "crv":
            curve_loader = CurveLoaderCrv(self._file_path, selections, self._log_curve_tags)
        elif curve_type == "csv":
            curve_loader = CurveLoaderCsv(self._file_path, selections, options, self._log_curve_tags)
        else:
            logging.error("unknown load curve type {}".format(curve_type))
            raise ValueError
        self._curve_loader = curve_loader

    def load_curves(self):
        self._curve_loader.generate()
        self._curves = self._curve_loader.curves

    def generate_store_data(self):
        self._store_data = RegisterCalculationData(curves=self._curves)

    def get_arguments(self):
        super().get_arguments()
        self._curve_extraction_input = self._extractor.get_value("curve_extraction")
        self._log_curve_tags = self._extractor.get_value("log_curve_tags")

    def generate(self):
        self.extract()
        super().generate()
        self.get_arguments()
        self.generate_curve_extraction()
        self.generate_curve_loader()
        self.load_curves()
        self.generate_store_data()
        self.store_in_register()
