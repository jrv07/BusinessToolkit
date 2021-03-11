from module_misc.BasicTask import BasicTask
from module_input.Curve.LoadCurvesSelection import LoadCurvesSelection
from module_input.Curve.Binout.LoadCurvesSelectionBinout import LoadCurvesSelectionBinout
from module_input.Curve.Crv.LoadCurvesSelectionCrv import LoadCurvesSelectionCrv
from module_input.Curve.Csv.LoadCurvesSelectionCsv import LoadCurvesSelectionCsv
from module_input.Curve.Csv.LoadOptionsCsv import LoadOptionsCsv
from typing import List
import logging


class CurveExtraction(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._type = None
        self._selections_input = None
        self._options_input = None
        self._extractor.add_str("type", valid_values=["binout", "crv", "csv"], optional=False, description="")
        self._extractor.add_list("selections", entry_type=dict, entry_object_type=LoadCurvesSelection, optional=False, description="")
        self._extractor.add_object("options", LoadOptionsCsv, description="")
        self._extractor.set_group_name("ReadData")
        self._selections: List[LoadCurvesSelection] = None
        self._options = None

    @property
    def type(self):
        return self._type

    @property
    def selections(self):
        return self._selections

    @property
    def options(self):
        return self._options

    def generate_selections(self):
        selections: List[LoadCurvesSelection] = []
        for selection_input in self._selections_input:
            if self._type == "binout":
                selection = LoadCurvesSelectionBinout(selection_input)
            elif self._type == "crv":
                selection = LoadCurvesSelectionCrv(selection_input)
            elif self._type == "csv":
                selection = LoadCurvesSelectionCsv(selection_input)
            else:
                logging.error("Unknown load curve type: {}".format(self._type))
                raise ValueError
            selection.generate()
            selections.append(selection)
        self._selections = selections

    def generate_options(self):
        if self._type == "binout":
            return
        elif self._type == "crv":
            return
        elif self._type == "csv":
            if self._options_input is None:
                logging.error("options for loading csv missing")
                raise ValueError
            options = LoadOptionsCsv(self._options_input)
        else:
            return
        options.generate()
        self._options = options

    def get_arguments(self):
        super().get_arguments()
        self._type = self._extractor.get_value("type")
        self._selections_input = self._extractor.get_value("selections")
        self._options_input = self._extractor.get_value("options")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_selections()
        self.generate_options()
